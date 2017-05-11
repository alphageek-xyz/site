from django.contrib import admin
from .models import Contact, STATUS_CHOICES


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter     = ('status', 'date',)
    list_display    = ('date', 'status', 'full_name', 'email', 'phone', 'comment',)
    actions         = ['mark_closed', 'mark_responded', 'mark_new', 'delete_selected']
    ordering        = ['-date', 'status',]
    date_hierarchy  = 'date'
    fields          = (
        'status', 'notes', 'full_name', 'date',
        'email', 'phone', 'comment',
        'remote_address'
    )

    readonly_fields = fields[2:]

    def change_status(self, status, request, queryset):
        choices = [x[0] for x in STATUS_CHOICES]
        if choices.count(status):
            rows_updated = queryset.update(status=status)
            if rows_updated == 1:
                message_bit = "1 isssue was"
            else:
                message_bit = "{0} issues were".format(rows_updated)
            self.message_user(request, "{0} successfully marked {1}.".format(
                message_bit, STATUS_CHOICES[choices.index(status)][1]
            ))

    def mark_closed(self, *args):
        self.change_status('c', *args)

    def mark_responded(self, *args):
        self.change_status('r', *args)

    def mark_new(self, *args):
        self.change_status('n', *args)

    def full_name(self, obj):
        return obj.name

    mark_closed.short_description    = 'Mark selected issues as closed'
    mark_responded.short_description = "Mark selected issues as responded to"
    mark_new.short_description       = "Mark selected issues as new"
    full_name.short_description      = "Full Name"
