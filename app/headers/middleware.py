from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_vary_headers, get_conditional_response
from django.utils.http import unquote_etag
from django import get_version
from django.conf import settings
from .utils.functional import set_headers
from django.middleware.http import ConditionalGetMiddleware


class GetIfNoneMatchMiddleware(ConditionalGetMiddleware): # pragma: no cover
    def process_response(self, request, response):
        if (not response.streaming and
            not response.has_header('Content-Length')
        ): response['Content-Length'] = str( # pragma: no cover
            len(response.content)
        )
        etag = response.get('ETag')
        if etag:
            return get_conditional_response(
                request,
                etag=unquote_etag(etag),
                response=response,
            )
        return response


class VaryAcceptEncodingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        newheaders = response.has_header('Vary') and ([
            s.strip() for s in response['Vary'].split(',')
        ]) or []
        newheaders.append('Accept-Encoding')
        patch_vary_headers(response, set(newheaders))
        return response


class ViaHeaderMiddleware(MiddlewareMixin):
    via_proxies = []

    def __init__(self, get_response=None):
        super(ViaHeaderMiddleware, self).__init__(get_response)
        self.proxies = self.via_proxies or getattr(
            settings, 'VIA_PROXIES', []
        ) or ['Django/%s' % get_version()]

    def process_response(self, request, response):
        set_headers(response, default=True, Via=', '.join(set(
            self.proxies + [request.META['SERVER_SOFTWARE']] if (
                'SERVER_SOFTWARE' in request.META
            ) else self.proxies
        )))
        return response


class MultipleProxyMiddleware(MiddlewareMixin):
    FORWARDED_FOR_FIELDS = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    ]

    def process_request(self, request):
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META:
                if ',' in request.META[field]:
                    parts = request.META[field].split(',')
                    request.META[field] = parts[-1].strip()
