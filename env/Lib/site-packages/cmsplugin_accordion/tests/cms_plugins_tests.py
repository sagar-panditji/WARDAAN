"""Tests for the CMSPlugins of the cmsplugin_accordion app."""
from django.test import TestCase

from . import factories
from .. import cms_plugins


class AccordionPluginTestCase(TestCase):
    """Tests for the ``AccordionPlugin`` class."""
    longMessage = True

    def test_plugin(self):
        plugin_model = factories.AccordionPluginFactory()
        plugin = cms_plugins.AccordionPlugin()
        result = plugin.render({}, plugin_model, None)
        self.assertEqual(result['instance'], plugin_model, msg=(
            'Should add the selected instance to the context'))
