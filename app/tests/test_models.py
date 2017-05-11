import re
from django.test import TestCase, Client
from django.contrib.sites.models import Site
from landing.models import Service, markup_markdown
from contact.models import Contact
from metadata.models import *
from django.core.exceptions import ValidationError
from collections import namedtuple


ok_fields = namedtuple('Data', [
    'first_name','last_name','comment','email', 'phone'
])(
    'Foo', 'bar', 'hello world', 'foo@bar.com', '1231231234'
)


class MetadataModelsTest(TestCase):

    fixtures = [
        'states.json',
        'tags.json',
        'links.json',
        'keywords.json',
        'phone_numbers.json',
        'postal_addresses.json',
    ]

    def setUp(self):
        site, created = Site.objects.get_or_create(
            domain='www.alphageek.xyz',
            name='www.alphageek.xyz'
        )
        self.site = site

    def test_create_website(self):
        business = LocalBusiness.objects.create(
            name='Test Alpha Geek Services',
            alt_name='Test AGCS',
            description='Hello World',
            url='www.alphageek.xyz',
            address=PostalAddress.objects.last(),
            telephone=PhoneNumber.objects.first(),
            logo='https://www.alphageek.xyz/s/img/logo.png',
            founder='Foo Bar',
            email='foo@example.com'
        )

        business.links.add(
            Link.objects.last(),
            Link.objects.first()
        )

        business.save()

        wsite = Website.objects.create(
            site=self.site,
            schema=business
        )

        wsite.keywords.add(
            *Keyword.objects.filter(pk__gt=1)
        )

        wsite.save()

        for f in Website._meta.fields:
            key = getattr(f, 'name', '')
            print("%s : %s" % (key, getattr(
                Website.objects.last(), key, ''
            )))


class LandingServiceModelTest(TestCase):

    fixtures = ['services.json']

    def test_markup_markdown(self):
        script_re = re.compile('<( +)?script')
        self.assertNotRegex(markup_markdown(self.description),
            script_re
        )
        self.assertRegex(self.description, script_re)

    def test_new_service(self):
        Service.objects.create(
            name='Test Service',
            description = "- foo\n- bar",
        )

    def test_save_with_explicit_order(self):
        last = Service.objects.last()
        s = Service(
            name='Test Service',
            description=self.description,
            order=last.order+1
        )
        s.save()
        self.assertEqual(s.order, last.order+1)

    @property
    def description(self):
        return """
# H1
## H2
### H3

<script>console.log("hello");</script>

- foo
- bar

```
<script>alert("Hello");</script>
<span class="foo">hello</span>
```

hello world
"""


class LandingContactModelTest(TestCase):

    def setUp(self):
        self.fields = ok_fields._asdict()

    def test_new_contact(self):
        c = Contact(**self.fields)
        c.full_clean()
        c.save()

    def test_bad_contact(self):
        self.fields.update({'email': ''})
        c = Contact(**self.fields)
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_changed_name_after_clean(self):
        c = Contact(**self.fields)
        c.full_clean()
        c.first_name = ''
        with self.assertRaises(ValidationError):
            c.full_clean()
        c.first_name = 'Baz'
        c.full_clean()
        c.save()
