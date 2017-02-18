import re
from django import forms
from .validators import validate_phone_number


class PhoneInput(forms.TextInput):
    input_type = 'tel'


class PhoneField(forms.CharField):
    widget = PhoneInput
    default_validators = [validate_phone_number]
    default_error_messages = {
        'invalid': 'Enter a valid phone number (xxx-xxx-xxxx).',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_length', 10)
        kwargs.setdefault('max_length', 14)
        kwargs.setdefault('label', 'Phone Number')
        super(PhoneField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = self.to_python(value).strip()
        return re.sub('\D', str(),
            super(PhoneField, self).clean(value)
        )[:10]
