from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm
)
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class MyAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )


class MyPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaWidget()
    )

