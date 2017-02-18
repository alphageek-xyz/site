import re
from string import digits
from django.core.validators import _lazy_re_compile
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
from django.forms import ValidationError


@deconstructible
class PhoneValidator(object):
    message = 'Enter a valid phone number.'
    code = 'invalid'
    area_code_regex = _lazy_re_compile(
        r"((\("
        r"(?P<f1>\d{3})"
        r"\)|"
        r"(?P<f2>\d{3})"
        r")( |-)?)"
    )
    main_digits_regex = _lazy_re_compile(
        r'(?P<p1>\d{3})'
        r'(?P<bad>-| )?'
        r'(?P<p2>\d{4})'
    )


    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code


    def __eq__(self, other):
        return (
            isinstance(other, PhoneValidator) and
            (self.message == other.message) and
            (self.code == other.code)
        )


    def __call__(self, value):
        value = force_text(value)

        if not value:
            raise ValidationError(self.message, code=self.code)

        if not all(i in digits+'()- ' for i in value):
            raise ValidationError(self.message, code=self.code)

        area_code_match = self.area_code_regex.match(value)

        if not area_code_match:
            raise ValidationError(self.message, code=self.code)

        area_code = area_code_match.group('f1') or area_code_match.group('f2')

        if not area_code:
            raise ValidationError(self.message, code=self.code)

        main_part_value = value[area_code_match.span()[-1]:]

        main_digits_match = self.main_digits_regex.match(main_part_value)

        if not main_digits_match:
            raise ValidationError(self.message, code=self.code)

        main_digits = main_digits_match.group('p1') + main_digits_match.group('p2')

        if not main_digits:
            raise ValidationError(self.message, code=self.code)

        remaining_chars = main_part_value[main_digits_match.span()[-1]:]

        if remaining_chars:
            raise ValidationError(self.message, code=self.code)

        if len(area_code+main_digits) != 10:
            raise ValidationError(self.message+'\n'+area_code+'  '+main_digits, code=self.code)


validate_phone_number = PhoneValidator()
