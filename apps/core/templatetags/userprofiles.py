from django import template

from apps.core.models import UserType


register = template.Library()

@register.simple_tag
def userprofile(request):
    return {
        'userprofile': UserType.objects.all()
    }