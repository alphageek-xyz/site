from django.utils.module_loading import import_string
from django.utils.decorators import decorator_from_middleware
from .functional import set_headers, del_headers


def with_headers(default=True, **headers):
    def _with_headers(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            set_headers(response, default, **headers)
            return response
        return wrapper
    return _with_headers


def without_headers(*headers):
    def _without_headers(view_func):
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            del_headers(response, *headers)
            return response
        return wrapper
    return _without_headers


def via_header(view_func):
    return decorator_from_middleware(
        import_string('headers.middleware.ViaHeaderMiddleware')
    )(view_func)
