"""Forms for the cmsplugin_accordion app."""
from django import forms

from . import models


class AccordionForm(forms.ModelForm):
    class Meta:
        model = models.Accordion
