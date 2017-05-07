import re
from django.forms import TextInput as FormTextInput
from django.forms import CharField as FormCharField
from django.db.models import CharField as ModelCharField
from django.core import validators
from .validators import validate_phone_number

class PhoneInput(FormTextInput):
    input_type = 'tel'


class FormPhoneField(FormCharField):
    widget = PhoneInput
    default_validators = [validate_phone_number]
    default_error_messages = {
        'invalid': 'Enter a valid phone number (xxx-xxx-xxxx).',
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_length', 10)
        kwargs.setdefault('max_length', 14)
        kwargs.setdefault('label', 'Phone Number')
        super(FormPhoneField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = self.to_python(value).strip()
        return re.sub('\D', str(),
            super(FormPhoneField, self).clean(value)
        )[:10]


class ModelPhoneField(ModelCharField):
    default_validators = [validate_phone_number]
    description = 'Phone Number'

    def __init__(self, *args, min_length=10, **kwargs):
        kwargs.setdefault('max_length', 14)

        if min_length < 10:
            self.min_length = 10
        else:
            self.min_length = min_length

        if kwargs['max_length'] < self.min_length:
            kwargs['max_length'] = self.min_length

        super(ModelPhoneField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MinLengthValidator(self.min_length))

    def deconstruct(self):
        name, path, args, kwargs = super(ModelPhoneField, self).deconstruct()
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': FormPhoneField,
            'min_length': self.min_length
        }
        defaults.update(kwargs)
        return super(ModelPhoneField, self).formfield(**defaults)
