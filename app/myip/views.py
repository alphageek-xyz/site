from django.http import HttpResponse
from django.views.decorators.cache import cache_page


@cache_page(10)
def my_ip_address(request, *args, **kwargs):
    try:
        del(request.session)
    except AttributeError:
        pass
    return HttpResponse(
        request.META.get('HTTP_X_REAL_IP', b''),
        content_type='text/html'
    )
