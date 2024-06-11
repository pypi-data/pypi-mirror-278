# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import typing
import socket
import asyncio
import functools

import grpc

from .server import GRPCServer, Router
from .server import GRPC_MODE_TYPE, UNARY_UNARY_MODE, UNARY_STREAM_MODE, STREAM_UNARY_MODE, STREAM_STREAM_MODE
from .client import GRPCClient

from ...extend.asyncio.base import Utils
from ...extend.asyncio.command import MainProcess, SubProcess


def copy_metadata(remote_context: grpc.aio.ServicerContext) -> grpc.aio.Metadata:

    metadata = grpc.aio.Metadata((r'remote-peer', remote_context.peer()))

    for _key, _value in remote_context.invocation_metadata():
        metadata.add(_key, _value)

    return metadata


class _ProxyUpstream:

    def __init__(
            self, remote_request: typing.AsyncIterator,
            server_stream_stub: typing.Union[grpc.aio.StreamUnaryCall, grpc.aio.StreamStreamCall]
    ):

        self.__remote_request: typing.AsyncIterator = remote_request

        self._upstream_stub: typing.Union[grpc.aio.StreamUnaryCall, grpc.aio.StreamStreamCall] = server_stream_stub
        self._upstream_task: asyncio.Task = asyncio.create_task(self._do_upstream_task())

    async def _do_upstream_task(self):

        try:
            async for _message in self.__remote_request:
                await self._upstream_stub.write(_message)
            await self._upstream_stub.done_writing()
        except Exception as err:
            Utils.log.exception(str(err))


class _ProxyDownstream:

    def __init__(
            self, remote_context: grpc.aio.ServicerContext,
            server_stream_stub: typing.Union[grpc.aio.UnaryStreamCall, grpc.aio.StreamStreamCall]
    ):

        self.__remote_context: grpc.aio.ServicerContext = remote_context

        self._downstream_stub: typing.Union[grpc.aio.UnaryStreamCall, grpc.aio.StreamStreamCall] = server_stream_stub
        self._downstream_task: asyncio.Task = asyncio.create_task(self._do_downstream_task())

    async def _do_downstream_task(self):

        remote_peer = self.__remote_context.peer()

        Utils.log.info(f'grpc proxy open stream: {remote_peer}')

        try:
            async for _message in self._downstream_stub:
                await self.__remote_context.write(_message)
        except grpc.aio.UsageError:
            pass
        except Exception as err:
            Utils.log.exception(str(err))
        finally:
            if self._downstream_stub is not None:
                self._downstream_stub.cancel()

        Utils.log.info(f'grpc proxy close stream: {remote_peer}')


class ProxyUnaryStream(_ProxyDownstream):

    def __init__(
            self, server_proxy: GRPCClient, server_method: str,
            remote_request: bytes, remote_context: grpc.aio.ServicerContext
    ):

        super().__init__(
            remote_context,
            server_proxy.unary_stream(
                server_method, remote_request,
                metadata=copy_metadata(remote_context)
            )
        )

    async def join(self) -> typing.Any:
        return await self._downstream_task


class ProxyStreamUnary(_ProxyUpstream):

    def __init__(
            self, server_proxy: GRPCClient, server_method: str,
            remote_request: typing.AsyncIterator, remote_context: grpc.aio.ServicerContext
    ):

        super().__init__(
            remote_request,
            server_proxy.stream_unary(
                server_method,
                metadata=copy_metadata(remote_context)
            )
        )

    async def join(self) -> typing.Any:
        return await self._upstream_stub


class ProxyStreamStream(_ProxyUpstream, _ProxyDownstream):

    def __init__(
            self, server_proxy: GRPCClient, server_method: str,
            remote_request: typing.AsyncIterator, remote_context: grpc.aio.ServicerContext
    ):

        server_stream_stub = server_proxy.stream_stream(
            server_method,
            metadata=copy_metadata(remote_context)
        )

        _ProxyUpstream.__init__(self, remote_request, server_stream_stub)
        _ProxyDownstream.__init__(self, remote_context, server_stream_stub)

    async def join(self) -> typing.Any:
        return await asyncio.wait([self._upstream_task, self._downstream_task])


class GRPCProxy:

    def __init__(
            self, address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router],
            grpc_family: int = socket.AF_INET, grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = None
    ):

        self._routers: typing.List[Router] = routers

        self._grpc_client: typing.Optional[GRPCClient] = None
        self._grpc_server: typing.Optional[GRPCServer] = None

        self._grpc_address: typing.Union[str, typing.Tuple[str, int]] = address
        self._grpc_family: int = grpc_family
        self._grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = grpc_server_credentials

    async def _unary_unary_handler(self, method: str, request: bytes, context: grpc.aio.ServicerContext) -> typing.Any:
        return await self._grpc_client.unary_unary(method, request, metadata=copy_metadata(context))

    async def _unary_stream_handler(self, method: str, request: bytes, context: grpc.aio.ServicerContext) -> typing.Any:
        return await ProxyUnaryStream(self._grpc_client, method, request, context).join()

    async def _stream_unary_handler(self, method: str, request: typing.AsyncIterator, context: grpc.aio.ServicerContext) -> typing.Any:
        return await ProxyStreamUnary(self._grpc_client, method, request, context).join()

    async def _stream_stream_handler(self, method: str, request: typing.AsyncIterator, context: grpc.aio.ServicerContext) -> typing.Any:
        return await ProxyStreamStream(self._grpc_client, method, request, context).join()

    def _get_handler(self, method: str, mode: GRPC_MODE_TYPE) -> grpc.RpcMethodHandler:

        handler = None

        if mode is UNARY_UNARY_MODE:
            handler = functools.partial(self._unary_unary_handler, method)
        elif mode is UNARY_STREAM_MODE:
            handler = functools.partial(self._unary_stream_handler, method)
        elif mode is STREAM_UNARY_MODE:
            handler = functools.partial(self._stream_unary_handler, method)
        elif mode is STREAM_STREAM_MODE:
            handler = functools.partial(self._stream_stream_handler, method)

        return mode(handler)

    def _init_handlers(self):

        self._grpc_server.register(r'', [self._join_node], mode=STREAM_STREAM_MODE)

        generic_handlers = []

        for router in self._routers:
            generic_handlers.append(
                grpc.method_handlers_generic_handler(
                    router.service,
                    {
                        _func.__name__: self._get_handler(f'/{router.service}/{_func.__name__}', _mode)
                        for _func, _mode in router.handlers
                    }
                )
            )

        self._grpc_server.server.add_generic_rpc_handlers(generic_handlers)

    async def _join_node(self, request: typing.AsyncIterator, context: grpc.aio.ServicerContext):

        target = dict(context.invocation_metadata()).get(r'worker_entry_point')

        if target:
            context.add_done_callback(lambda _: Utils.create_task(self._grpc_client.clear_targets([target])))
        else:
            await context.abort(grpc.StatusCode.CANCELLED)

        await self._grpc_client.append_target(target)

        Utils.log.success(f'grpc proxy connected worker: {target}')

        with Utils.suppress(grpc.RpcError):
            async for _message in request:
                Utils.log.warning(f'grpc proxy received message: {_message}')

    async def open(self):

        self._grpc_client: GRPCClient = GRPCClient(request_serializer=None, response_deserializer=None)
        self._grpc_server: GRPCServer = GRPCServer(request_deserializer=None, response_serializer=None)

        self._init_handlers()

        await self._grpc_server.start(self._grpc_address, self._grpc_family, self._grpc_server_credentials)

    async def close(self):

        await self._grpc_server.stop()
        await self._grpc_client.close()

    async def join(self):
        await self._grpc_server.wait()


class GRPCEntry:

    def __init__(self, proxy_address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router]):

        self._proxy_address: str = self._decode_address(proxy_address)
        self._server_address: str = f'/tmp/grpc_node_{Utils.getpid()}.sock'

        self._grpc_server: typing.Optional[GRPCServer] = None
        self._grpc_routers: typing.List[Router] = routers

        self._proxy_client: typing.Optional[GRPCClient] = None
        self._proxy_client_stub: typing.Optional[grpc.aio.StreamStreamCall] = None

    @staticmethod
    def _decode_address(proxy_address: typing.Union[str, typing.Tuple[str, int]]) -> str:

        if isinstance(proxy_address, str):
            proxy_address = Utils.split_str(proxy_address, r':')

        if proxy_address[0] == r'0.0.0.0':
            proxy_address =(r'localhost', proxy_address[1])

        return Utils.join_str(proxy_address, r':')

    async def start(self):

        if os.path.exists(self._server_address):
            os.remove(self._server_address)

        self._grpc_server = GRPCServer()

        for _router in self._grpc_routers:
            self._grpc_server.bind_router(_router)

        await self._grpc_server.start(self._server_address, family=socket.AF_UNIX)

        self._proxy_client = GRPCClient()
        await self._proxy_client.open([self._proxy_address])

        self._proxy_client_stub = self._proxy_client.stream_stream(
            r'//_join_node',
            metadata=grpc.aio.Metadata((r'worker_entry_point', r'unix:' + self._server_address))
        )

    async def stop(self):
        await self._proxy_client.close()
        await self._grpc_server.stop()

    async def join(self):

        with Utils.suppress(grpc.RpcError):
            async for _message in self._proxy_client_stub:
                Utils.log.warning(f'grpc worker received message: {_message}')

        await self._grpc_server.wait()


class GRPCMainProcess(MainProcess):

    def __init__(
            self, address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router],
            worker: typing.Type[r'GRPCWorker'], sub_process_num: int, *,
            grpc_family: int = socket.AF_INET, grpc_server_credentials: typing.Optional[grpc.ServerCredentials] = None,
            cpu_affinity: bool = False, join_timeout: int = 10
    ):

        super().__init__(
            worker.create, sub_process_num,
            cpu_affinity=cpu_affinity, join_timeout=join_timeout,
            proxy_address=address, routers=routers
        )

        self._grpc_proxy: GRPCProxy = GRPCProxy(address, routers, grpc_family, grpc_server_credentials)

    async def initialize(self):
        await self._grpc_proxy.open()

    async def release(self):
        await self._grpc_proxy.close()


class GRPCWorker(SubProcess):

    def __init__(self, process_num: int, proxy_address: typing.Union[str, typing.Tuple[str, int]], routers: typing.List[Router]):

        super().__init__(process_num)

        self._grpc_entry: GRPCEntry = GRPCEntry(proxy_address, routers)

    async def initialize(self):
        await self._grpc_entry.start()

    async def release(self):
        await self._grpc_entry.stop()

    async def _execute(self):
        await self._grpc_entry.join()
