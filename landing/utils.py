import bleach
import markdown
from bs4 import BeautifulSoup
from django.conf import settings

def markup_markdown(md, allowed_tags=None, allowed_attrs=None):
    html = bleach.clean(markdown.markdown(
        md, extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.wikilinks',
            'markdown.extensions.smart_strong',
            'markdown.extensions.smarty',
            'markdown.extensions.extra',
            'pymdownx.magiclink',
            'pymdownx.betterem',
            'pymdownx.tilde',
            'pymdownx.superfences',
        ]),
        styles=['width', 'margin'],
        tags=allowed_tags or bleach.ALLOWED_TAGS + [
            'h1', 'h2', 'h3', 'h4', 'p',
            'div', 'pre', 'small', 'img'
        ],
        attributes=allowed_attrs or {
            'a':       ['href', 'title', 'target', 'class'],
            'abbr':    ['title'],
            'acronym': ['title'],
            'div':     ['class', 'name'],
            'p':       ['class', 'name'],
            'img':     ['alt', 'src', 'class', 'id', 'height', 'width'],
        }
    )

    soup = BeautifulSoup(
        '<div class="service-markup">\n%s\n</div>' % html,
        'html.parser'
    )
    for ul in soup.select('ul'):
        ul['class'] =  'list-group'
    for li in soup.select('ul li'):
        li['class'] = 'bullet-item'
    for h in ['h%d' % i for i in range(1, 5)]:
        for t in soup.select(h):
            t['class'] = 'text-primary'

    return str(soup)
