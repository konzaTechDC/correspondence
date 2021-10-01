from .models import Notification
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader  import render_to_string
from django.conf import settings 



def create_notification(request, to_user, notification_type, extra_id=0):
    notification = Notification.objects.create(to_user=to_user, notification_type=notification_type, created_by=request.user, extra_id=extra_id)

# TODO
# [] EMAIL NOTI FUNC