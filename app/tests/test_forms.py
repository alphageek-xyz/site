import os
from django.core import mail
from django.test import TestCase, override_settings
from contact import forms as contact_forms
from .test_models import ok_fields


class ContactFormTest(TestCase):

    def setUp(self):
        self.data = ok_fields._asdict()
        self.bad = self.data.copy()
        del(self.bad['first_name'])


    def test_valid_form(self):
        response = self.client.post(
            '/contact/', self.data, follow=True
        )

        self.assertEqual(200,
            response.status_code
        )

        self.assertEqual(1,
            len(mail.outbox)
        )

        self.assertEqual(mail.outbox[0].subject,
            str(' '.join(('Contact Form:',
                self.data['first_name'],
                self.data['last_name'],
            )))
        )


    def test_invalid_form(self):
        response = self.client.post(
            '/contact/', self.bad, follow=True
        )

        self.assertEqual(200,
            response.status_code
        )

        self.assertFormError(response,
            'form', 'first_name', 'This field is required.'
        )


    @override_settings(ADMINS=(('Foo Bar', 'foo@bar.com\nyut'),))
    def test_bad_email_header(self):
        form = contact_forms.ContactForm(self.data)

        self.assertTrue(
            form.is_valid()
        )

        ret = form.send_email()

        self.assertIsInstance(ret,
            contact_forms.HttpResponse
        )

        self.assertEqual(200,
            ret.status_code
        )

        self.assertRegex(ret.content.decode(),
            r'BadHeaderError'
        )

        self.assertEqual(0,
            len(mail.outbox)
        )
