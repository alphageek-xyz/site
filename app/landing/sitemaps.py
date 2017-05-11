from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class LandingSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['services', 'contact']

    def location(self, item):
        return reverse(item)

