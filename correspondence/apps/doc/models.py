from django.db import models
from django.contrib.auth.models import User 

from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

CATEGORIES = [
	('M', 'Memo'),
	('L', 'Letters'),
	# ('')
]

MANAGER = 'manager'
CHIEF_MANAGER = 'cm'
CEO = 'ceo'
STORES = 'stores'

RECEIVER_TYPE = (
    (MANAGER, 'Manager'),
    (CHIEF_MANAGER, 'Cm'),
    (CEO, 'Ceo'),
    (STORES, 'Stores'),
)


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(max_length=100)
    document = models.FileField(null=True, blank=True, upload_to='Files')
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse('file-detail', kwargs={'pk': self.pk})

class ForwardFile(models.Model):
    file = models.ForeignKey(Document, related_name='documents', on_delete=models.CASCADE)
    # sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30, choices=RECEIVER_TYPE, default=MANAGER)
    comment = models.TextField()

    created_by = models.ForeignKey(User, related_name='documents', on_delete=models.CASCADE)
    forwarded_at = models.DateTimeField(auto_now_add=True)

    