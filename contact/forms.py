import copy
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (
    EmailMultiAlternatives,
    BadHeaderError,
    get_connection
)
from django.template.loader import render_to_string
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import Contact
from .utils import mkemail
from .fields import FormPhoneField

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name',
            'phone', 'email', 'comment',
        ]

    cc_myself = forms.BooleanField(
        required=False,
        initial=False,
    )

    captcha = ReCaptchaField(
        widget=ReCaptchaWidget(
            callback='enableSubmit',
            expired_callback='disableSubmit'
        )
    )

    def send_email(self, request=None):

        emails = [EmailMultiAlternatives(**{
            'subject'    : 'Contact Form: ' + str(self.instance.name),
            'to'         : [mkemail(*a) for a in settings.ADMINS],
            'reply_to'   : [mkemail(str(self.instance.name), self.cleaned_data['email'])],
            'body'       : str().join('{0:15s} : {1}\n'.format(
                            self.fields[f].label, self.cleaned_data[f])
                            for f in self._meta.fields),
        })]

        emails[0].attach_alternative(
            render_to_string('contact/email.html',
                context={
                    'name'    : str(self.instance.name),
                    'phone'   : self.cleaned_data['phone'],
                    'email'   : self.cleaned_data['email'],
                    'comment' : self.cleaned_data['comment'],
                },
                request=request
            ), 'text/html'
        )

        if self.cleaned_data['cc_myself']:
            emails.append(copy.copy(emails[0]))
            emails[1].to = emails[0].reply_to
            emails[1].reply_to = [settings.DEFAULT_REPLY_ADDR]

        try:
            with get_connection() as con:
                con.send_messages(emails)
                con.close()
        except BadHeaderError as e:
            return HttpResponse(' '.join(
                ['BadHeaderError:'] + list(e.args)
            ))
        except Exception as e: # pragma: no cover
            print(e)
            return False
        return True
