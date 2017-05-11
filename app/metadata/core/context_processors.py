from django.conf import settings
from metadata.models import Website


def links(request):
    try:
        return {
            'links': dict(
                Website.objects.get(
                    site__name=settings.DEFAULT_WEBSITE_NAME
                ).schema.links.filter(
                    tags__name='social'
                ).values_list(
                    'name', 'url'
                )
            )
        }
    except (AttributeError, Website.DoesNotExist):
        return {}

def _website():
    try:
        return {
            'site': Website.objects.get(
                site__name=settings.DEFAULT_WEBSITE_NAME
            )
        }
    except (AttributeError, Website.DoesNotExist):
        return {
            'site': Website.objects.first()
        }

def website(request):
    return _website()
