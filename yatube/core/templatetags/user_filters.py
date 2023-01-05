from django import template
from django.forms import BoundField

register = template.Library()


@register.filter
def addclass(field: BoundField, css) -> BoundField:
    return field.as_widget(attrs={'class': css,},)
