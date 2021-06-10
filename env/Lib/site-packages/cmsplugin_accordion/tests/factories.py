"""Factories for the cmsplugin_accordion app."""
import factory

from .. import models


class AccordionPluginFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.AccordionPlugin

    name = factory.Sequence(lambda n: 'name {0}'.format(n))


class AccordionRowFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.AccordionRow

    accordion = factory.SubFactory(AccordionPluginFactory)
    title = factory.Sequence(lambda n: 'title {0}'.format(n))
