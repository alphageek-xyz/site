from __future__ import unicode_literals
import datetime
from pathlib import Path
from django.template import loader
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView, TemplateView
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.http import last_modified
from contact.views import ContactView
from landing.views import LandingPageView
from landing.sitemaps import LandingSitemap
from landing.models import Service
from community.sitemaps import ForumsSitemap, TopicsSitemap
from headers.utils.decorators import with_headers
from django.contrib.auth.views import login as login_view
from django.contrib.auth import views as authviews
from landing.forms import MyAuthenticationForm, MyPasswordResetForm
from metadata.core.context_processors import login_kwargs
from landing.views import ovpnfile
from metadata.models import Website


def fp_lastmod(request, url):
    return datetime.datetime.fromtimestamp(
        Path(loader.get_template(
            FlatPage.objects.get(url=url).template_name
            or "flatpages/default.html"
        ).template.origin.name).stat().st_mtime
    )


sitemaps = {
    'flatpages': FlatPageSitemap,
    'landing': LandingSitemap,
    'forums': ForumsSitemap,
    'topics': TopicsSitemap,
}


urlpatterns = [

    url(r'^$',
        cache_page(60*5)(last_modified(fp_lastmod)(flatpage)),
        kwargs={'url': '/'},
        name='home'
    ),

    url(r'^about/$',
        cache_page(60*5)(last_modified(fp_lastmod)(flatpage)),
        kwargs={'url': '/about/'},
        name='about'
    ),

    url(r'^about/privacy/$',
        cache_page(60*5)(last_modified(fp_lastmod)(flatpage)),
        kwargs={'url': '/about/privacy/'},
        name='privacy'
    ),

    url(r'^about/terms/$',
        cache_page(60*5)(last_modified(fp_lastmod)(flatpage)),
        kwargs={'url': '/about/terms/'},
        name='terms'
    ),

    url(r'^user/blank/$',
        never_cache(flatpage),
        kwargs={'url': '/user/blank/'},
        name='user_blank'
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

    url(r'^shop/$',
        LandingPageView.as_view(
            template_name='pages/shop.html'
        ),
        name='shop'
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

    url(r'^docs/public/',
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

    url(r'accounts/login/$',
        authviews.login,
        kwargs=login_kwargs(authentication_form=MyAuthenticationForm),
        name='login'
    ),

    url(r'accounts/logout/$',
        authviews.logout,
        kwargs=login_kwargs(next_page='/'),
        name='logout'
    ),

    url(r'^accounts/password_change/$',
        authviews.password_change,
        kwargs=login_kwargs(),
        name='password_change'
    ),

    url(r'^accounts/password_change/done/$',
        authviews.password_change_done,
        kwargs=login_kwargs(),
        name='password_change_done'
    ),

    url(r'^accounts/password_reset/$',
        authviews.password_reset,
        kwargs=login_kwargs(password_reset_form=MyPasswordResetForm),
        name='password_reset'
    ),

    url(r'^accounts/password_reset/done/$',
        authviews.password_reset_done,
        kwargs=login_kwargs(),
        name='password_reset_done'
    ),

    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        authviews.password_reset_confirm,
        kwargs=login_kwargs(),
        name='password_reset_confirm'
    ),

    url(r'^accounts/reset/done/$',
        authviews.password_reset_complete,
        kwargs=login_kwargs(),
        name='password_reset_complete'
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
