import re
from django.db import models
from django.core import validators
from django.utils.functional import cached_property
from tagging.registry import register
from landing.utils import markup_markdown
from tagging.fields import TagField


class AnnouncementManager(models.Manager):
    def last_modified(self):
        return self.latest('modified').modified


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name


class Link(models.Model):
    class Meta:
        ordering = ('order',)
        get_latest_by = 'modified'

    name = models.CharField(
        max_length=200
    )

    href = models.URLField(
        max_length=500,
        verbose_name='HREF'
    )

    order = models.IntegerField(
        null=True,
    )

    modified = models.DateTimeField(
        auto_now=True,
    )

    @cached_property
    def anchor_id(self):
        return re.sub(
            " ?[&/\\@ ]+ ?", '_', self.name
        )[:30]

    def get_absolute_url(self):
        from django.urls import reverse
        return '%s#%s' % (reverse('links'), self.anchor_id)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = 1 + (
                Link.objects.aggregate(
                    n=models.Max('order')
                )['n'] or 0
            )
        return super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Announcement(models.Model):

    class Meta:
        get_latest_by = "date"

    title = models.CharField(
        max_length=100,
        unique=True
    )

    content = models.TextField(
        blank=True,
    )

    order = models.IntegerField(
        null=True
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True,
    )

    display_title = models.BooleanField(
        default=True
    )

    @cached_property
    def html(self):
        return markup_markdown(
            self.content
        )

    @cached_property
    def anchor_id(self):
        return re.sub(
            " ?[&/\\@ ]+ ?", '_', self.title
        )[:30]

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = 1 + (
                Announcement.objects.aggregate(
                    n=models.Max('order')
                )['n'] or 0
            )
        return super(Announcement, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

register(Link)
