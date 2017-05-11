from django.contrib import admin
from .models import *


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    ordering = ('name',)


@admin.register(PostalAddress)
class PostalAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_string',)

    def address_string(self, obj):
        return str(obj)

    address_string.short_description = 'Address'


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number_string', 'kind',)
    list_filter = ('kind',)

    def number_string(self, obj):
        return str(obj)

    number_string.short_description = 'Phone Number'


@admin.register(LocalBusiness)
class LocalBusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    pass

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    fields = readonly_fields = ['id', 'name', 'abbreviation']
    list_display = ['id', 'name', 'abbreviation']
