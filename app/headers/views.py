from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition


class NeverCacheMixin(object): # pragma: no cover
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object): # pragma: no cover
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class CSRFExemptMixin(object): # pragma: no cover
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)


class CacheControlMixin(object):
    cache_timeout = None

    def patch_response(self, response):
        if self.cache_timeout:
            patch_response_headers(response, self.cache_timeout)


class ConditionalViewMixin(object):
    last_modified_func = None
    etag_func = None

    def get_conditional_response(self, *args, **kwargs):
        return condition(
            self.etag_func,
            self.last_modified_func
        )(super(self.__class__, self).dispatch)(
            *args, **kwargs
        )
