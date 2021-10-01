"""correspondence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from datetime import datetime
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from apps.core.views import index
from django.contrib.auth.views import LoginView, LogoutView
# from apps.core.views import profile_reg
#signup -> removed signup view import
from apps.core import forms
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='home'),
    # path('signup/', profile_reg, name='signup'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # path('login/', login_view, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dashboard/', include('apps.userprofile.urls')),
    path('document/', include('apps.doc.urls')),
    path('notifications/', include('apps.notification.urls')),

]


# change site header
admin.site.site_header = 'Correspondence Administration'
admin.site.index_title = 'Manage Correspondences'