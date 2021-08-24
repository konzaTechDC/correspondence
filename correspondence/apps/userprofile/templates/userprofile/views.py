from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from apps.jobs.models import Job
from apps.userprofiles.models import UserProfile

def home(request):
    jobs = Job.objects.all()[4:]

    return render(request, 'core/index.html', {'jobs':jobs})

def signup(request):

    # check the request when submit is clicked
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # CHECK VALID FORM ,SAVE, login user
        if form.is_valid():
            user = form.save()
            # check account type
            account_type = request.POST.get('account_type', 'jobseeker')#default->job-seeler

            if account_type == 'employer':
                userprofile = UserProfile.objects.create(user=user, is_employer=True)
                # user.userprofile.is_employer = True 
                userprofile.save()
            else:
                userprofile = UserProfile.objects.create(user=user)
                userprofile.save()

            login(request, user)

            return redirect('dashboard')
        
        else:
            form = UserCreationForm()

    return render(request, 'core/signup.html', {'form':form})