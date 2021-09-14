from apps.core.models import User 
from django.db import models

class Manager(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='manager', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_shares(self):
        '''get all files shared with the manager'''
        pass

    def get_shared(self):
        ''' get all files shared by me '''
        pass
