from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import decorator_from_middleware
from django.test import (
    TestCase,
    RequestFactory,
    modify_settings,
    override_settings,
)
from headers.middleware import (
    MultipleProxyMiddleware,
    ViaHeaderMiddleware,
)


def goodview(request, *args, **kwargs):
    return HttpResponse(
        "Hello world",
        content_type="text/html"
    )


class HeadersMiddleWareTest(TestCase):

    def setUp(self):
        self.rf = RequestFactory()

    def test_with_extra_meta(self):
        req = self.rf.get('/')
        for f in getattr(
            MultipleProxyMiddleware,
            'FORWARDED_FOR_FIELDS'
        ): req.META[f] = 'Value1'
        del(req.META['HTTP_X_FORWARDED_SERVER'])
        req.META['HTTP_X_FORWARDED_FOR'] += ',Foo'
        req.META['SERVER_SOFTWARE'] = 'foo/1.1'
        viawrap = decorator_from_middleware(ViaHeaderMiddleware)
        mulwrap = decorator_from_middleware(MultipleProxyMiddleware)
        viawrap(mulwrap(goodview))(req)

    @override_settings(USE_ETAGS=False)
    def test_without_etags(self):
        res = self.client.get(
            reverse('contact'),
            CONTENT_LENGTH=123
        )
        self.assertEqual(200, res.status_code)
        self.assertFalse(res.has_header('ETag'))
