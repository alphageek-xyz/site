from django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from headers.views import ConditionalViewMixin, CacheControlMixin
from .models import Service


@never_cache
@login_required
@permission_required('auth.can_view_vpn_config', raise_exception=True)
def ovpnfile(request):
    return render(request, 'text/vpn.alphageek.xyz.ovpn', content_type='text/plain')


class LandingPageView(ConditionalViewMixin, CacheControlMixin, TemplateView):
    last_modified_func = lambda *a: Service.objects.last_modified()

    def get_context_data(self, **kwargs):
        try:
            has_services = 'landing.core.context_processors.services' in (
                import_string('django.template.engines').templates
                    ['django']['OPTIONS']['context_processors']
            )
        except (KeyError, AttributeError):
            has_services = False
        if not has_services:
            kwargs.update({
                'service_list': Service.objects.all(),
            })
        return super(LandingPageView, self).get_context_data(**kwargs)


    def dispatch(self, *args, **kwargs):
        response = self.get_conditional_response(*args, **kwargs)
        self.patch_response(response)
        return response
