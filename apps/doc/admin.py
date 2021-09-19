from django.contrib import admin
from .models import Document, Category, ForwardFile, Department

admin.site.register(Document)
admin.site.register(Category)
admin.site.register(ForwardFile)
admin.site.register(Department)