from django.urls import path 
from .views import (dashboard, view_shared, manager, fileUpdate,read_notification,
                        UserFileListView, FileDeleteView, timeline)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('manager/', manager, name='manager'),
    path('shared/<int:file_id>/', view_shared, name='view_shared'),
    path('user/<str:username>', UserFileListView.as_view(), name='user-files'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),
    # path('file/<int:pk>/update/', FileUpdateView.as_view(), name='file-update'),
    path('file/<int:file_id>/update/', fileUpdate, name='file-update'),
    path('read/', read_notification, name='read-notification'),
    path('timeline/', timeline, name="timeline"),
]