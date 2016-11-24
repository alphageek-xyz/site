from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property


STATUS_CHOICES = (
    ('r', 'Responded'),
    ('c', 'Closed'),
    ('n', 'New'),
)


class Contact(models.Model):

    class Meta:
        get_latest_by = "date"

    date = models.DateTimeField(
        auto_now_add=True
    )

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=20,
        unique=False,
        validators=[
            validators.MinLengthValidator(2),
            validators.RegexValidator(
                '^[aA-zZ]+\Z$',
                message='Enter a valid first name.',
                code='invalid',
            ),
        ],
    )

    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=20,
        unique=False,
        validators=[
            validators.MinLengthValidator(2),
            validators.RegexValidator(
                '^[aA-zZ]+$',
                message='Enter a valid last name.',
                code='invalid',
            ),
        ],
    )

    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=10,
        validators=[
            validators.MinLengthValidator(10),
            validators.int_list_validator(
                sep='',
                message='Enter a valid phone number (Only Integers).'
            ),
        ],
    )

    email = models.CharField(
        verbose_name='Email Address',
        max_length=100,
        validators=[
            validators.EmailValidator(
                message='Enter a valid email.',
                code='invalid'
            ),
        ],
    )

    comment = models.TextField(
        verbose_name='Comment',
        validators=[
            validators.MinLengthValidator(4,
                message='Type at least 1 word (4 characters)',
            ),
        ]
    )

    status = models.CharField(
        default='n',
        max_length=1,
        choices=STATUS_CHOICES
    )

    notes = models.CharField(
        null=True,
        blank=True,
        verbose_name='Admin Notes',
        max_length=200
    )

    remote_address = models.GenericIPAddressField(
        verbose_name='Remote IP',
        null=True,
        blank=True
    )

    @cached_property
    def name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        if self.date:
            return '{0} : {1}'.format(
                self.name,
                self.date.strftime('%Y-%m-%d %H:%M:%S')
            )
        return self.name
