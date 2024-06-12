from ajsonrpc.core import JSONRPC20DispatchException

from zhixin.compat import aio_to_thread
from zhixin.home.rpc.handlers.base import BaseRPCHandler
from zhixin.registry.client import RegistryClient


class RegistryRPC(BaseRPCHandler):
    @staticmethod
    async def call_client(method, *args, **kwargs):
        try:
            client = RegistryClient()
            return await aio_to_thread(getattr(client, method), *args, **kwargs)
        except Exception as exc:  # pylint: disable=bare-except
            raise JSONRPC20DispatchException(
                code=5000, message="Registry Call Error", data=str(exc)
            ) from exc
