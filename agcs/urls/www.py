from __future__ import unicode_literals
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView, TemplateView
from django.views.decorators.cache import cache_page
from contact.views import ContactView
from landing.views import LandingPageView
from landing.sitemaps import LandingSitemap
from community.sitemaps import ForumsSitemap, TopicsSitemap
from headers.utils.decorators import with_headers


sitemaps = {
    'flatpages': FlatPageSitemap,
    'landing': LandingSitemap,
    'forums': ForumsSitemap,
    'topics': TopicsSitemap,
}


urlpatterns = [

    url(r'^$',
        cache_page(60*5)(flatpage),
        kwargs={'url': '/'},
        name='home'
    ),

    url(r'^about/$',
        cache_page(60*5)(flatpage),
        kwargs={'url': '/about/'},
        name='about'
    ),

    url(r'^about/privacy/$',
        cache_page(60*5)(flatpage),
        kwargs={'url': '/about/privacy/'},
        name='privacy'
    ),

    url(r'^about/terms/$',
        cache_page(60*5)(flatpage),
        kwargs={'url': '/about/terms/'},
        name='terms'
    ),

    url(r'^(?P<url>shared/.*)$',
        flatpage,
        name='shared'
    ),

    url(r'^contact/$',
        ContactView.as_view(
            success_url='/contact/',
            template_name = 'pages/contact.html'
        ),
        kwargs={'gapi_key' : getattr(settings, 'GOOGLE_API_KEY', None)},
        name='contact'
    ),

    url(r'^services/$',
        with_headers(False, X_Robots_Tag='noarchive')(
            LandingPageView.as_view(
                template_name='pages/services.html',
                cache_timeout=settings.DEBUG and 5 or 300
            )
        ),
        name='services'
    ),

    url(r'^robots\.txt$',
        TemplateView.as_view(
            content_type='text/plain',
            template_name='robots.txt',
        ),
        name='robots'
    ),

    url(r'^sitemap\.xml$',
        cache_page(60*60)(sitemap),
        kwargs={'sitemaps': sitemaps}
    ),

    url(r'^manifest\.json$', cache_page(60*60)(
        TemplateView.as_view(
            content_type='application/json',
            template_name='manifest.json'
        )),
        kwargs={'prefix': getattr(settings, 'FAVICON_PREFIX', None)},
        name='chrome_manifest'
    ),

    url(r'^treenav/',
        include('treenav.urls')
    ),

    url(r'^docs/',
        include('pubdocs.urls')
    ),

    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')
    ),

    url(r'^admin/',
        admin.site.urls
    ),

    url(r'^community/',
        include('community.urls')
    ),
]

if settings.DEBUG:
    urlpatterns.extend([
        url(r'^favicon\.ico$',
            RedirectView.as_view(
                url=staticfiles_storage.url('img/favicon.ico'),
                permanent=False
            ),
            name='favicon'
        ),
    ])
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
