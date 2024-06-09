from drakaina.middleware.base import BaseMiddleware
from drakaina.types import ASGIReceive
from drakaina.types import ASGIScope
from drakaina.types import ASGISend
from drakaina.types import ProxyRequest
from drakaina.types import WSGIEnvironment
from drakaina.types import WSGIResponse
from drakaina.types import WSGIStartResponse


class RequestWrapperMiddleware(BaseMiddleware):
    """The middleware for wrapping the request object.

    Provides access to the mapping environment object through
    the attribute access interface. This is needed for some
    backward compatibility in cases where the request is
    an object with attributes, such as `request.user`.

    """

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        return self.app(ProxyRequest(environ), start_response)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ):
        await self.app(ProxyRequest(scope), receive, send)
