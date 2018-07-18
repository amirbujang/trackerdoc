from django import template
from documents.models import EventPermission

register = template.Library()

@register.filter()
def action_permission(event, user):
    groups = user.groups.all()

    return event.eventpermission_set.filter(group__in=groups, allow=True).exists()

@register.filter()
def create_permission(user):
    groups = user.groups.all()
    return EventPermission.objects.filter(event__name="Baru", group__in=groups, allow=True).exists()

@register.filter()
def edit_permission(user):
    groups = user.groups.all()
    allow = EventPermission.objects.filter(event__name="Edit", group__in=groups, allow=True).exists()
    print("Edit", allow)
    return allow

@register.filter()
def delete_permission(user):
    groups = user.groups.all()
    allow = EventPermission.objects.filter(event__name="Delete", group__in=groups, allow=True).exists()
    print("Delete:", allow)
    return allow
