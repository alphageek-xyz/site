import os, re, json
from django.conf import settings
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe, format_html
from django.contrib.staticfiles import finders
from bootstrap3.templatetags.bootstrap3 import bootstrap_form, bootstrap_field
from css_html_js_minify.html_minifier import html_minify
from css_html_js_minify.css_minifier import css_minify
from css_html_js_minify.js_minifier import js_minify


register = Library()


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
