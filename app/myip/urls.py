from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import url, include
from .views import my_ip_address

urlpatterns = [
    url(r'^', my_ip_address, name='myip'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
