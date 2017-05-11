from django.contrib import sitemaps
from machina.apps.forum.models import Forum
from community.apps.forum_conversation.models import Post, Topic
from django.core.urlresolvers import reverse

class ForumsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Forum.objects.all()

    def lastmod(self, obj):
        return obj.last_post_on

    def location(self, item):
        return reverse('forum:forum', kwargs={
            'pk': item.pk,
            'slug': item.slug
        })


class TopicsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Topic.objects.filter(approved=True, status=0)

    def lastmod(self, obj):
        return obj.updated

    def location(self, item):
        return reverse('forum_conversation:topic', kwargs={
            'pk': item.pk,
            'slug': item.slug,
            'forum_pk': item.forum.pk,
            'forum_slug': item.forum.slug,
        })
