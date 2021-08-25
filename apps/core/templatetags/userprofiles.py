from django import template

from apps.userprofile.models import UserProfile


register = template.Library()

@register.simple_tag
def userprofile(request):
    return {
        'userprofile': UserProfile.objects.all()
    }