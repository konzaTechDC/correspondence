from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  AuthenticationForm   
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from apps.core.models import UserType
from apps.doc.models import ForwardFile
from django.core.mail import send_mail
from django.conf import settings

from .forms import ProfileForm, InfoProfileForm

@login_required
def index(request):
    if request.user.is_authenticated and UserType.objects.get(user=request.user).is_admin:
        return HttpResponseRedirect(reverse('dashboard'))
    elif request.user.is_authenticated and UserType.objects.get(user=request.user).is_manager:
        files = ForwardFile.objects.all()
        return render(request, 'userprofile/manager_dashboard.html', {'files':files})
    return render(request, 'core/index.html')


    
def profile_reg(request):
    register = False
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST)
        info_form = InfoProfileForm(data=request.POST)

        if profile_form.is_valid() and info_form.is_valid():
            user = profile_form.save()
            user.set_password(user.password)
            user.save()


            profile = info_form.save(commit=False)
            # profile.user = user 
            profile.save()

            subject = "Your Account Registration"
            message = f"Hello, {user.first_name}. You have been registered with our application. Please use login to..."
            to = user.email

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to],
            )
            
            register=True

            return redirect('home')
        else:
            HttpResponse(messages.warning(request, 'Something went wrong'))

    else:
        profile_form = ProfileForm(data=request.POST)
        info_form = InfoProfileForm(data=request.POST)
    
    return render(request, 'core/registration.html', 
            {'profile_form':profile_form,
            'info_form': info_form,
            'register':register,
            })