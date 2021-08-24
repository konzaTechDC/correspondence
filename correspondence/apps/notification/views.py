from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notification

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True 
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('view_forwarded', file_id=notification.extra_id)
        
        elif notification.notification_type == Notification.FORWARD:
            return redirect('view_forwarded', file_id=notification.extra_id)

    return render(request, 'notification/notification.html')