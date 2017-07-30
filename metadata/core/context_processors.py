from django.conf import settings
from metadata.models import Website

def login_kwargs(**kwargs):
    site=Website.objects.first()
    links=dict(site.schema.links.filter(tags__name='social').values_list('name', 'url'))
    retdict={}
    retdict.update(kwargs)
    extra_context={'links':links}
    extra_context.update({'site': site})
    retdict.update({'extra_context': extra_context})
    return retdict

def _links():
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


def links(request):
    return _links()


def website(request):
    return _website()
