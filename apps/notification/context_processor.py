from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.filter(is_read=False)}
    
    else:
        return {'notifications': []}

def read_notifications(request):
    if request.user.is_authenticated:
        return {'read_notifications': request.user.notifications.filter(is_read=True)}
    
    else:
        return {'read_notifications': []}