from django.urls import path, include 

from .views import upload_doc, file_detail, forward_file,manager_forward, FileDetailView

urlpatterns = [
    path('add/', upload_doc, name='new_file'),
    path('file/<int:pk>/', FileDetailView.as_view(), name="file_detail"),
    path('forward/<int:file_id>', forward_file, name="forward_file"),
    path('manager_forward/<int:file_id>', manager_forward, name="manager_forward"),


]