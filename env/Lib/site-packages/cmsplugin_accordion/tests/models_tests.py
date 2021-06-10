"""Tests for the models of the cmsplugin_accordion app."""
from django.test import TestCase

from . import factories


class AccordionRowTestCase(TestCase):
    """Tests for the ``AccordionRow`` model class."""
    def test_model(self):
        obj = factories.AccordionRowFactory()
        self.assertTrue(obj.pk)


class AccordionPluginModelTestCase(TestCase):
    """Tests for the ``AccordionPluginModel`` model class."""
    def test_model(self):
        obj = factories.AccordionPluginFactory()
        self.assertTrue(obj.pk)
