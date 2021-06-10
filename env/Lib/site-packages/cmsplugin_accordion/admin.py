"""Admin classes for the cmsplugin_accordion app."""
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from cms.admin.placeholderadmin import PlaceholderAdmin

from . import models


# ADMIN INLINES ===============================================================
# =============================================================================
class AccordionRowInline(admin.TabularInline):
    model = models.AccordionRow
    exclude = ['content', ]
    fields = ['title', 'content_link', 'position', ]
    readonly_fields = ['content_link', ]

    def content_link(self, obj):
        if not obj.pk:
            return _('Please save first...')
        url = reverse(
            'admin:cmsplugin_accordion_accordionrow_change', args=[obj.pk, ])
        link = '<a href="{0}" target="_blank">Edit content</a>'.format(url)
        return mark_safe(link)


# MODEL ADMINS ================================================================
# =============================================================================
class AccordionPluginAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]
    inlines = [AccordionRowInline, ]


class AccordionRowAdmin(PlaceholderAdmin):
    list_display = ['title', 'accordion__name', 'position', ]
    list_editable = ['position', ]
    list_filter = ['accordion', ]
    search_fields = ['title', 'accordion__name', ]

    def accordion__name(self, obj):
        return obj.accordion.name
    accordion__name.short_description = _('Accordion')


admin.site.register(models.AccordionPlugin, AccordionPluginAdmin)
admin.site.register(models.AccordionRow, AccordionRowAdmin)
