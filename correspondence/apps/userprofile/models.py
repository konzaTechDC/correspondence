from django.db import models
from apps.core.models import User 
from apps.doc.models import ForwardFile


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_cm = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)
    is_stores = models.BooleanField(default=False)


    

User.userprofile = property(lambda u:UserProfile.objects.get_or_create(user=u)[0])


class ConversationMessage(models.Model):
    send = models.ForeignKey(ForwardFile, related_name='conversationmessages', on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name='conversationmaessages', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']