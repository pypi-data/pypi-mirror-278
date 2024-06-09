from __future__ import annotations

from drakaina.types import ASGIApplication
from drakaina.types import ASGIReceive
from drakaina.types import ASGIScope
from drakaina.types import ASGISend
from drakaina.types import WSGIApplication
from drakaina.types import WSGIEnvironment
from drakaina.types import WSGIResponse
from drakaina.types import WSGIStartResponse


__all__ = ("BaseMiddleware",)


class BaseMiddleware:
    """Base class for middleware.

    It is a simple middleware for WSGI and ASGI, where the protocol
    will be chosen depending on the `is_async` parameter.

    :param app:
    :type app: WSGIApplication | ASGIApplication
    """

    __slots__ = ("app", "is_async", "__call__")

    def __init__(
        self,
        app: ASGIApplication | WSGIApplication,
        is_async: bool = False,
    ):
        self.app = app
        self.is_async = is_async
        if is_async:
            self.__call__ = self.__asgi_call__
        else:
            self.__call__ = self.__wsgi_call__

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        return self.app(environ, start_response)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ):
        await self.app(scope, receive, send)
