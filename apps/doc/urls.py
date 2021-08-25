from django.urls import path, include 

from .views import upload_doc, file_detail, forward_file

urlpatterns = [
    path('add/', upload_doc, name='new_file'),
    path('file/<int:file_id>', file_detail, name="file_detail"),
    path('forward/<int:file_id>', forward_file, name="forward_file"),

    # path('<int:job_id>/apply_for_job', apply_for_job, name='apply_for_job'),
]