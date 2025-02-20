# housing_app/templatetags/group_tags.py

from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Usage in the template:
        {% load group_tags %}
        {% if user|has_group:"Volunteer" %}
            ...
        {% endif %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()
