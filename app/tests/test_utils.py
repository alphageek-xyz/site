from django.test import TestCase, override_settings, RequestFactory
from django_hosts.resolvers import reverse
from headers.utils.functional import (
    set_headers,
    del_headers,
    get_uwsgi_version,
    get_gunicorn_version,
)
from headers.utils.decorators import (
    with_headers,
    without_headers,
    via_header,
)
from myip.views import my_ip_address


class HeadersUtilsTest(TestCase):

    @property
    def foo_via_force_headers_func(self):
        return with_headers(
            default=False, Foo='bar',
        )(via_header(my_ip_address))

    @property
    def foo_via_headers_func(self):
        return with_headers(
            default=True, Foo='bar'
        )(via_header(my_ip_address))

    def setUp(self):
        self.rf = RequestFactory()

    def test_add_headers(self):
        res = self.foo_via_headers_func(
            self.rf.get('/')
        )
        self.assertTrue(res.has_header('Foo'))
        self.assertTrue(res.has_header('Via'))
        self.assertEqual(res['Foo'], 'bar')
        self.assertIn('Django', res['Via'])

    def test_force_headers(self):
        res = self.foo_via_force_headers_func(
            self.rf.get('/')
        )
        self.assertTrue(res.has_header('Foo'))
        self.assertTrue(res.has_header('Via'))
        self.assertEqual(res['Foo'], 'bar')
        self.assertIn('Django', res['Via'])

    def test_del_headers(self):
        res = without_headers('Foo', 'Via', 'Bar')(
            self.foo_via_headers_func
        )(self.rf.get('/'))
        self.assertFalse(res.has_header('Foo'))
        self.assertFalse(res.has_header('Via'))

    def test_get_server_versions(self):
        self.assertTrue(get_uwsgi_version() is not None)
        self.assertTrue(get_gunicorn_version() is None)
