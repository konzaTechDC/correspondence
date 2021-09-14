from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from apps.userprofile.models import UserProfile
from apps.doc.models import Document
# from django.contrib.sessions.backends import file
from django.contrib.auth.forms import  AuthenticationForm   
import logging

logging.basicConfig(filename='user_login.log', filemode='w', level=logging.DEBUG)

def index(request):
    files = Document.objects.all()

    return render(request, 'core/index.html', {'files':files})


def signup(request):

    if request.method == 'POST':
        form = UserRegForm(request.POST)

        if form.is_valid():
            user = form.save()

            account_type = request.POST.get('account_type', 'admin')

            if account_type == 'manager':
                userprofile = UserProfile.objects.create(user=user, is_manager=True)
                userprofile.save()
            elif account_type == 'cm':
                userprofile = UserProfile.objects.create(user=user, is_cm=True)
                userprofile.save()
            elif account_type == 'ceo':
                userprofile = UserProfile.objects.create(user=user, is_ceo=True)
                userprofile.save()
            elif account_type == 'stores':
                userprofile = UserProfile.objects.create(user=user, is_stores=True)
                userprofile.save()
            else:
                userprofile = UserProfile.objects.create(user=user)
                userprofile.save()

            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Your account has been created! You are now able to log in')

            login(request, user)
        
            return redirect('dashboard')

    else:
        form = UserRegForm()

    return render(request, 'core/signup.html', {'form':form})

def login_view(request):
    try:

        form = AuthenticationForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user is not None: # is not None and user.is_manager == True
                login(request, user)
                # check if there is next request -> to get a specific page such as dashboard
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('manager_dashboard')

        return render(request, 'core/login.html', {'form':form})

    except Exception as e:
        logging.error(e)