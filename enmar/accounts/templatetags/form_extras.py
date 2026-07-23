from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """
    Usage in template:
      {{ form.username|add_class:"class1 class2" }}
    Adds the given css classes to the field widget HTML.
    """
    try:
        return field.as_widget(attrs={"class": css})
    except Exception:
        # If something goes wrong, fall back to default rendering
        return field