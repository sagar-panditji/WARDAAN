"""CMSPlugins for the cmsplugin_accordion app."""
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models
from . import admin


class AccordionPlugin(CMSPluginBase):
    inlines = [admin.AccordionRowInline, ]
    model = models.AccordionPlugin
    name = _('Accordion Plugin')
    render_template = "cmsplugin_accordion/accordion_plugin.html"

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(AccordionPlugin)
