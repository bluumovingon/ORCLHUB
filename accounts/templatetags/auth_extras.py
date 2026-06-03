from django import template
from django.contrib.auth.models import Group

register = template.Library()

# ----------------- CHECKER FUNCTIONS FOR @user_passes_test -----------------

def is_admin(user):
    """
    Checks if a user has admin rights. 
    Admins are users in the 'Admin' group or who are superusers.
    """
    if not user or not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_editor(user):
    """
    Checks if a user is in the 'Editor' group.
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Editor').exists()

def is_user(user):
    """
    Checks if a user is in the 'User' group.
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='User').exists()

def is_admin_or_editor(user):
    """
    Checks if a user is either an Admin or an Editor.
    """
    return is_admin(user) or is_editor(user)


# ----------------- CUSTOM TEMPLATE FILTERS -----------------

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Filter to check if a user belongs to a specific group in templates.
    Usage: {% if request.user|has_group:"Editor" %}
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

@register.filter(name='is_admin')
def filter_is_admin(user):
    """
    Filter to check if a user is an admin.
    Usage: {% if request.user|is_admin %}
    """
    return is_admin(user)

@register.filter(name='is_editor')
def filter_is_editor(user):
    """
    Filter to check if a user is an editor.
    Usage: {% if request.user|is_editor %}
    """
    return is_editor(user)

@register.filter(name='is_regular_user')
def filter_is_regular_user(user):
    """
    Filter to check if a user is a regular user.
    A regular user is one that belongs to the 'User' group, or does not belong to any group/role, 
    and is not an admin, editor, staff, or superuser.
    Usage: {% if request.user|is_regular_user %}
    """
    if not user or not user.is_authenticated:
        return False
    if is_admin(user) or is_editor(user) or user.is_staff or user.is_superuser:
        return False
    return user.groups.filter(name='User').exists() or not user.groups.exists()
