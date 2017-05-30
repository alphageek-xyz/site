from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.views import serve
from django.views.generic.base import TemplateView
from .views import DocumentCreate, DocumentUpdate, DocumentDelete

urlpatterns = [
    url(r'$',
        TemplateView.as_view(
            template_name='treenav_base.html'
        ), name='public-docs'
    ),
]

if settings.DEBUG:
    urlpatterns += url(r'^(?P<path>.*)$',
        serve, name='doc-detail'
    )
