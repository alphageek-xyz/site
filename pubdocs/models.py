import os.path
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


def user_dir_path(instance, filename):
    return 'docs/{0}'.format(os.path.basename(filename))


class AbstractDocument(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='docs',
        related_query_name='doc'
    )

    file = models.FileField(
        upload_to=user_dir_path
    )

    slug = models.SlugField(
        'slug',
        unique=True,
        max_length=255,
        help_text="Unique identifier for this document"
    )

    info = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        abstract = True
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.filename)

    @property
    def filename(self):
        return os.path.basename(getattr(self.file, 'name', ''))


class Document(AbstractDocument):
    def get_absolute_url(self):
        return self.file.storage.url(self.file.name)
