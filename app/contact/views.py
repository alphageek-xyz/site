from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
from .models import Contact
from .forms import ContactForm

class ContactView(FormView):
    form_class = ContactForm

    def form_valid(self, form):
        form.instance.remote_address = self.request.META.get(
            'HTTP_X_REAL_IP', '0.0.0.0'
        )
        try:
            self.object = form.save()
            form.send_email(request=self.request)
        except: # pragma: no cover
            messages.error(self.request,
                'An internal server error occured.',
                extra_tags='form_invalid',
            )
        else:
            messages.success(self.request,
                'Thanks! Someone will contact you soon.',
                extra_tags='form_valid',
            )
        return super(ContactView, self).form_valid(form)
