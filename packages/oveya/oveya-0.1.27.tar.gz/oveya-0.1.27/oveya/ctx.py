from typing import Any, Dict, Callable
import contextvars

from .request import Request


class RequestContext:
    def __init__(self):
        self._storage: Dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        return self._storage.get(name)

    def __setattr__(self, name: str, value: Any):
        if name == "_storage":
            super().__setattr__(name, value)
        else:
            self._storage[name] = value

    def __delattr__(self, name: str):
        if name in self._storage:
            del self._storage[name]

# Create a context variable for the request context
request_context_var = contextvars.ContextVar('request_context', default=RequestContext())


def get_request_context() -> RequestContext:
    return request_context_var.get()


def get_request() -> Request:
    return get_request_context().request


class RequestContextMiddleware:
    def __init__(self, app: Callable):
        self.app = app

    def __call__(self, event: Dict[str, Any]) -> Dict[str, Any]:
        token = request_context_var.set(RequestContext())
        try:
            req_ctx = get_request_context()
            req_ctx.request = Request(event)
            response = self.app(event)
        finally:
            request_context_var.reset(token)
        return response
