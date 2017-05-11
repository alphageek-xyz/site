import bleach
import markdown
from bs4 import BeautifulSoup
from django.conf import settings


_MARKDOWN_SETTINGS = {
    'ul_classes' : ['list-group'],
    'li_classes' : ['bullet-item'],
    'hx_classes' : ['text-primary'],
    'extensions': [
        'markdown.extensions.tables',
        'markdown.extensions.abbr',
        'markdown.extensions.smarty',
        'pymdownx.magiclink',
        'pymdownx.betterem',
        'pymdownx.tilde',
        'pymdownx.superfences',
    ],
}


def markup_markdown(md, allowed_tags=None):
    html = bleach.clean(markdown.markdown(
        md, extensions=list(getattr(settings,
            'MARKDOWN_EXTENSTIONS',
            _MARKDOWN_SETTINGS['extensions']
        ))), tags=allowed_tags or bleach.ALLOWED_TAGS + [
            'h%d' % i for i in range(1, 4)
        ] + ['p', 'div', 'pre']
    )
    soup = BeautifulSoup(
        '<div class="service-markup">\n%s\n</div>' % html,
        'html.parser'
    )
    for ul in soup.select('ul'):
        ul['class'] =  ' '.join(list(getattr(settings,
            'MARKDOWN_UL_CLASSES',
            _MARKDOWN_SETTINGS['ul_classes']
        )))
    for li in soup.select('ul li'):
        li['class'] = ' '.join(list(getattr(settings,
            'MARKDOWN_LI_CLASSES',
            _MARKDOWN_SETTINGS['li_classes']
        )))
    for h in ['h%d' % i for i in range(1, 4)]:
        for t in soup.select(h):
            t['class'] = ' '.join(list(getattr(settings,
                'MARKDOWN_HX_CLASSES',
                _MARKDOWN_SETTINGS['hx_classes']
            )))
    return str(soup)
