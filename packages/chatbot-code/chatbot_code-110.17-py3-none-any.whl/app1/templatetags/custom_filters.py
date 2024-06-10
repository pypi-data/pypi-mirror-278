# custom_filters.py

from django import template
import os
register = template.Library()

@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css})




@register.filter
def filename(value):
    return os.path.basename(value)
