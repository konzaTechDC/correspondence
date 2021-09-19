from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  AuthenticationForm   
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.core.models import UserType

@login_required
def index(request):
    if request.user.is_authenticated and UserType.objects.get(user=request.user).is_admin:
        return HttpResponseRedirect(reverse('dashboard'))
    elif request.user.is_authenticated and UserType.objects.get(user=request.user).is_manager:
        return render(request, 'userprofile/manager_dashboard.html')
    return render(request, 'core/index.html')


    
