from django.contrib import admin

from url_shortener.baseconv import base10to62
from url_shortener.models import ShortURL


class ShortURLAdmin(admin.ModelAdmin):
    def short_url(self, obj):
        return base10to62.from_decimal(obj.id)

    short_url.short_description = 'Short URL'

    list_display = ('short_url', 'date_submitted', 'usage_count')
    readonly_fields = ('date_submitted', 'usage_count')
    date_hierarchy = 'date_submitted'


admin.site.register(ShortURL, ShortURLAdmin)
