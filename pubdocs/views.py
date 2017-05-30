from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
    FormView
)
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from headers.views import NeverCacheMixin
from .models import Document


class RestrictedDocumentMixin(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    NeverCacheMixin
):
    model = Document
    login_url = '/admin/login/'
    permission_required = (
        'pubdocs.can_add',
        'pubdocs.can_delete',
    )

    permission_denied_message = """\
File uploads/modifications are restricted to authorized
users. Please contact the system administrator if you
think you have reached this page in error.
    """.strip().replace('\n', ' ')


class DocumentCreate(RestrictedDocumentMixin, CreateView):
    fields = ['file', 'slug', 'info']
    template_name = 'upload_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            self.object = form.save()
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
        return super(DocumentCreate, self).form_valid(form)


class DocumentUpdate(RestrictedDocumentMixin, UpdateView):
    fields = ['file', 'slug', 'info']
    template_name = 'upload_form.html'

class DocumentDelete(RestrictedDocumentMixin, DeleteView):
    model = Document

