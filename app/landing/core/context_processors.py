import json
from django.conf import settings
from landing.models import Service

def extra(request):
    extra = {
       'favicon_prefix': settings.FAVICON_PREFIX
    } if getattr(settings, 'FAVICON_PREFIX', None) else {}

    return { 'extra': extra }

def services(request):
    return {
        'service_list': Service.objects.all(),
    }
