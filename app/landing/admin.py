from django.contrib import admin
from django.db.models import F, Max
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('order', 'name', 'description',)
    list_display = ('name', 'order', 'modified',)
    ordering = ('order',)
    readonly_fields = ('order', 'modified',)
    actions = ['move_to_top', 'move_to_bottom', 'save_selection']

    def move_to_top(self, request, queryset):
        self.move_to_x('top', request, queryset)

    def move_to_bottom(self, request, queryset):
        self.move_to_x('bottom', request, queryset)

    def save_selection(self, request, queryset):
        for service in queryset:
            service.save()
        self.message_user(request,
            'Successfully saved %s.' % (
                ', '.join(s.name for s in queryset)
            )
        )

    def move_to_x(self, where, request, queryset):
        if queryset.count() > 1:
            self.message_user(request,
                'Please select only one service'
            )
            return

        target = (where == 'top') and 1 or (
            Service.objects.aggregate(
                n=Max('order')
            )['n'] or 1
        )

        selection = queryset.last()

        if selection.order == target:
            self.message_user(request,
                '%s is already at the %s!' % (
                selection.name, where
            ))
            return

        if where == 'top':
            Service.objects.filter(
                order__lt=selection.order
            ).update(order=F('order') + 1)
        else:
            Service.objects.filter(
                order__gt=selection.order
            ).update(order=F('order') - 1)

        selection.order = target
        selection.save()
        self.message_user(request,
            'Successfully moved "{}" to the {}'.format(
                selection.name, where
            )
        )

    move_to_top.short_description    = 'Move Service to top'
    move_to_bottom.short_description = 'Move Service to bottom'
    save_selection.short_description = 'Save selected services'
