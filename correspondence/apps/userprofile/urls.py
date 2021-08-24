from django.urls import path 
from .views import dashboard, view_shared, manager_dashboard, UserFileListView, FileDeleteView

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('', manager_dashboard, name='manager_dashboard'),
    path('shared/<int:file_id>/', view_shared, name='view_shared'),
    path('user/<str:username>', UserFileListView.as_view(), name='user-files'),
    path('file/<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),

]