"""middleware.py."""

import logging
from typing import Any, Awaitable, Callable, Coroutine

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from strangeworks_core.errors.error import StrangeworksError

from sw_product_lib.apps.context import SchedulerRequestContext
from sw_product_lib.service import RequestContext


logger = logging.getLogger()
# items in open_paths do not require any authentication.
open_paths = ["/docs", "/openapi.json", "/"]


class StrangeworksMiddleware(BaseHTTPMiddleware):
    """Middleware for handling interations between apps and the SW platform.

    Creates context objects from incoming requests which are used to communicate with
    the platform product API's. User requests are expected to have a proxy jwt token
    which is validated (if the app is not running in development-mode) before its claims
    are used to create a RequestContext object. Requests from the Google Cloud Scheduler
    are expected to have a valid token for the service account making the request.
    """

    def __init__(
        self,
        *args,
        user_paths: list[str] = [],
        scheduler_paths: list[str] = [],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.user_paths = user_paths
        self.scheduler_paths = scheduler_paths

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Coroutine[Any, Any, Response]:
        """Dispatch Strangeworks Requests

        Creates a context object which is used to make calls to the platform product
        API. If the application si s

        Parameters
        ----------
        request: Request
            The request to the application. Commonly from a user via the platform or
            Google Cloud Scheduler.
        call_next: Callable
            The handler method to call after middleware.

        Returns
        -------
        : Awaitable
            An Awaitable object from the next handler.
        """

        if request.url.path in self.user_paths:
            logger.debug("generating user RequestContext from request")
            # using RequestContext for now. Switch over to UserRequestContext
            # once all the apps are ready.
            ctx: RequestContext = RequestContext.from_request(request=request)
            request.state.ctx = ctx
        elif request.url.path in self.scheduler_paths:
            logger.debug("generating SchedulerRequestContext from request")
            ctx: SchedulerRequestContext = SchedulerRequestContext.from_request(
                request=request
            )
            request.state.ctx = ctx
        elif request.url.path not in open_paths:
            logger.fatal(
                (
                    f"Unable to route path: {request.url.path}."
                    "If the path is for handling a user request, it should be included "
                    "in user_paths. If its used by a scheduler, add it to "
                    "scheduler_paths."
                )
            )
            raise StrangeworksError(
                message=(
                    f"Unable to authorize path: {request.url.path}."
                    "If the path is for handling a user request, it should be added to "
                    "user_paths. If the path is for handling scheduler requests, it "
                    "should be included in scheduler_paths"
                )
            )
        return await call_next(request)
