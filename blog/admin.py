from django.contrib import admin
from django.db.models import F, Max
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    fields = ('order', 'title', 'content', 'display_title',)
    list_display = ('title', 'order', 'modified',)
    ordering = ('order',)
    readonly_fields = ('order', 'modified',)
    actions = ['move_to_top', 'move_to_bottom', 'save_selection']

    def move_to_top(self, request, queryset):
        self.move_to_x('top', request, queryset)

    def move_to_bottom(self, request, queryset):
        self.move_to_x('bottom', request, queryset)

    def save_selection(self, request, queryset):
        for announcement in queryset:
            announcement.save()
        self.message_user(request,
            'Successfully saved %s.' % (
                ', '.join(s.title for s in queryset)
            )
        )

    def move_to_x(self, where, request, queryset):
        if queryset.count() > 1:
            self.message_user(request,
                'Please select only one announcement'
            )
            return

        target = (where == 'top') and 1 or (
            Announcement.objects.aggregate(
                n=Max('order')
            )['n'] or 1
        )

        selection = queryset.last()

        if selection.order == target:
            self.message_user(request,
                '%s is already at the %s!' % (
                selection.title, where
            ))
            return

        if where == 'top':
            Announcement.objects.filter(
                order__lt=selection.order
            ).update(order=F('order') + 1)
        else:
            Announcement.objects.filter(
                order__gt=selection.order
            ).update(order=F('order') - 1)

        selection.order = target
        selection.save()
        self.message_user(request,
            'Successfully moved "{}" to the {}'.format(
                selection.title, where
            )
        )

    move_to_top.short_content    = 'Move Announcement to top'
    move_to_bottom.short_content = 'Move Announcement to bottom'
    save_selection.short_content = 'Save selected announcements'

