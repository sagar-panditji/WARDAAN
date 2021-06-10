"""Just an empty models file to let the testrunner recognize this as app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin


class AccordionPlugin(CMSPlugin):
    """
    Main object that groups several accordion elements together.

    :name: Unique name to make Accordion instances easier to select in the
      plugin admin.

    """
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=256,
        help_text=_(
            'Try to keep this name unique. It will help you distinguish'
            ' different accordions from each other in the Django admin'),
    )

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class AccordionRow(models.Model):
    """
    Each Accordion consists of n AccordionRows.

    An AccordionRow contains a title which will be shown when it is collapsed
    and some content which will be shown when it is expanded.

    :accordion: The Accordion instance this row belongs to.
    :title: The title that should be rendered when this row is collapsed.
    :content: The content that should be rendered when this row is expanded.
    :position: The position of this row in the give Accordion.

    """
    accordion = models.ForeignKey(
        'cmsplugin_accordion.AccordionPlugin',
        verbose_name=_('Accordion'),
        related_name='accordion_rows',
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=512,
    )

    content = PlaceholderField('accordion_row_content')

    position = models.PositiveIntegerField(
        blank=True, null=True,
    )

    class Meta:
        ordering = ('accordion__name', 'position', 'title', )

    def __unicode__(self):
        return '{0} - {1}'.format(self.accordion.name, self.title)
