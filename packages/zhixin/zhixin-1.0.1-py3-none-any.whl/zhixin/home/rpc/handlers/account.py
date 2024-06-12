from ajsonrpc.core import JSONRPC20DispatchException

from zhixin.account.client import AccountClient
from zhixin.home.rpc.handlers.base import BaseRPCHandler


class AccountRPC(BaseRPCHandler):
    @staticmethod
    def call_client(method, *args, **kwargs):
        try:
            client = AccountClient()
            return getattr(client, method)(*args, **kwargs)
        except Exception as exc:  # pylint: disable=bare-except
            raise JSONRPC20DispatchException(
                code=5000, message="ZX Account Call Error", data=str(exc)
            ) from exc
