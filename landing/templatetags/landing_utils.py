import os, re, json
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.html import format_html
from django.contrib.staticfiles import finders
from bootstrap3.templatetags.bootstrap3 import bootstrap_form, bootstrap_field
from css_html_js_minify.html_minifier import html_minify
from css_html_js_minify.css_minifier import css_minify
from css_html_js_minify.js_minifier import js_minify
from django.utils.safestring import mark_safe
from django.template.base import token_kwargs, TemplateSyntaxError
from django.template.loader_tags import IncludeNode, construct_relative_path
from django.template.library import Library


register = Library()


class CompressedIncludeNode(IncludeNode):

    def __init__(self, template, *args, **kwargs):
        self.compress_type = kwargs.pop('compress_type', 'html')
        super(CompressedIncludeNode, self).__init__(template, *args, **kwargs)

    def render(self, context):
        compress_func = html_minify
        if self.compress_type == 'js':
            compress_func = js_minify
        elif self.compress_type == 'css':
            compress_func = css_minify
        else:
            compress_func = html_minify

        return mark_safe(compress_func(
            super(CompressedIncludeNode, self).render(context)
        ))


@register.tag
def include_compressed(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )
    compress_types =  ['js', 'css', 'html']
    options = {}
    remaining_bits = bits[2:]

    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError('The %r option was specified more '
                                      'than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least '
                                          'one keyword argument.' % bits[0])
        elif option == 'only':
            value = True

        elif option in compress_types:
            unused = compress_types.copy()
            unused.remove(option)
            for t in unused:
                options[t] = False
            value = True
            options['type'] = option

        else:
            raise TemplateSyntaxError('Unknown argument for %r tag: %r.' %
                                      (bits[0], option))
        options[option] = value

    if not "type" in options:
        TemplateSyntaxError("'html','css' or 'js' not specified "
                            "for %r tag." % bits[0])

    compress_type = options.get('type', 'html')
    isolated_context = options.get('only', False)
    namemap = options.get('with', {})

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    return CompressedIncludeNode(parser.compile_filter(bits[1]), extra_context=namemap,
                       isolated_context=isolated_context,
                       compress_type=compress_type)


@register.simple_tag
def dict_to_json(pydict):
    """
    Accepts a python dict and returns it's JSON representation.

    Sample usage::

        <script type="application/ld+json">
            {% dict_to_json some_dict %}
        </script>
    """
    return mark_safe(json.dumps(pydict))


@register.simple_tag
def inline_static_file(path, minify=None):
    """
    Outputs the [minified] contents of a given static file.

    For example, to display the minified CSS file "``inline.css``"::

        <style>
            {% inline_static_file 'inline.css' 'css' %}
        </style>

    The optional ``minify`` argument can be one of css, js, or html.
    """
    p = finders.find(path)

    if not p:
        raise RuntimeError('path=%s not found' % path)
    elif os.path.isdir(p):
        raise RuntimeError('path=%s is not a file' % path)

    with open(p, encoding='utf-8') as f:
        if minify == 'js':
            return mark_safe(js_minify(f.read()))
        elif minify == 'css':
            return mark_safe(css_minify(f.read()))
        elif minify == 'html':
            return mark_safe(html_minify(f.read()))
        else:
            return mark_safe(f.read())


@register.simple_tag
def async_css(href):
    """
    Outputs a link and noscript tag, which will asynchronously load an external stylesheet.

    Sample usage::

        <head>
        ...
            {% async_css '/static/foo.css' %}
        ...
        </head>

    Results in::

        <head>
        ...
            <link rel="preload" href="/static/foo.css" onload="this.rel='stylesheet'">
            <noscript><link rel="stylesheet" href="/static/foo.css"></noscript>
        ...
        </head>
    """
    return format_html(''.join([
        '<link rel="preload" href="{0}" as="style" onload="this.rel=\'stylesheet\'">',
        '<noscript><link rel="stylesheet" href="{0}"></noscript>'
    ]), href)


@register.simple_tag
def autofocus_form(form, *args, **kwargs):
    """
    Add the 'autofocus' attribute to the first input tag of a form.

    Usage::

        {% autofocus_form form form_group_class='row' %}

    Extra args and kwargs are passed to ``bootstrap_form``.
    """
    return mark_safe(re.sub(
        '<input', '<input autofocus',
        str(bootstrap_form(form, *args, **kwargs)),
        count=1
    ))


@register.simple_tag
def autofocus_field(field, *args, **kwargs):
    """
    Add the 'autofocus' attribute to an input tag.

    Usage::

        {% autofocus_field field field_class='col-md-12' %}

    Extra args and kwargs are passed to ``bootstrap_field``.
    """
    return mark_safe(re.sub(
        '<input', '<input autofocus',
        str(bootstrap_field(field, *args, **kwargs)),
        count=1
    ))


@register.filter
@stringfilter
def mkanchorid(value):
    return mark_safe(re.sub(
        " ?[&/\\@ ]+ ?", '_',
        value)[:30]
    )

@register.filter
@stringfilter
def minify_js(value):
    return mark_safe(js_minify(value))


@register.filter
@stringfilter
def minify_css(value):
    return mark_safe(css_minify(value))


@register.filter
@stringfilter
def minify_html(value):
    return mark_safe(html_minify(value))


@register.filter
def listsort(value):
    return sorted(value)


@register.filter
def listsortreversed(value):
    return sorted(value, reverse=True)


@register.filter
@stringfilter
def split(value, char=','):
    return value.split(char)


@register.filter
@stringfilter
def find(value, substr):
    return value.find(substr)
