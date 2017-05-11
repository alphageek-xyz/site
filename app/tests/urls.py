from __future__ import unicode_literals
from agcs.urls.www import *

urlpatterns.append(
    url(r'^no-cache-services/$',
        with_headers(False, X_Robots_Tag='noarchive')(
            LandingPageView.as_view(
                template_name='pages/services.html',
                cache_timeout=None
            )
        ), name='no-cache-services'
    )
)
