from django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from headers.views import ConditionalViewMixin, CacheControlMixin
from .models import Service


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
