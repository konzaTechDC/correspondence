from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader  import render_to_string

from django.views.generic import ListView, DetailView

import datetime

from .forms import DocumentUploadForm, FileFowardForm

from .models import Document, ForwardFile, Category
from apps.core.models import User 
from apps.core.models import Profile

from apps.notification.utilities import create_notification

@login_required
def upload_doc(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST)
        if form.is_valid():
            upload = form.save(commit=False)

            # if form['category'] != 'none':
            #     Category.objects.get(id=form['category'])
            # elif form['add_category'] != '':
            #     category, created = Category.get_or_create(name=form['add_category'])
            # else:
            #     category = None
            upload.created_by = request.user
            upload.save()

            #success notification
            messages.success(request, 'Document Uploaded successfully.')      
            return redirect('new_file')
    else:
        form = DocumentUploadForm()

    return render(request, 'doc/add_file.html', {'categories':categories, 'form':form})

class FileDetailView(DetailView):
    model = Document
    context_object_name = 'document_detail'
    query_set = Document.objects.all()
    template_name = 'doc/document_detail.html'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.created_by:
            return True
        return False

def file_detail(request, file_id):
    file = get_object_or_404(Document, pk=file_id, created_by=request.user)

    return render(request, 'doc/file_detail.html', {'file':file})



def forward_file(request, file_id):
    file = Document.objects.get(pk=file_id)
    profile = Profile.objects.filter(user=request.user)
    users = User.objects.all()
    if request.method == 'POST':
        form = FileFowardForm(request.POST)

        if form.is_valid():
            forward = form.save(commit=False)
            forward.file = file 

            try:
                forward.receiver = User.objects.get(pk=int(request.POST.get('receiver', '')))
            except (ValueError, User.DoesNotExist) as e:
                return e

            forward.created_by = request.user
            forward.save()

            subject = f'{request.user.first_name} {request.user.last_name} Forwarded a {file.category.name}'
            from_email = settings.EMAIL_HOST_USER
            to = forward.receiver.email
            template = render_to_string('doc/email_template.html', 
                                            {'name': forward.receiver.first_name, 'category': file.category.name, 'title':file.title})
            text_content = 'You have a new message'
            msg = EmailMultiAlternatives(subject, text_content,from_email, [to])
            msg.attach_alternative(template, 'text/html')
            msg.send()

            create_notification(request, forward.receiver, 'forward', extra_id=forward.id)

            messages.success(request, f"{file.category.name} Forwarded successfuly to {forward.receiver}")

            return redirect('dashboard')
    
    else:
        form = FileFowardForm()
        
    return render(request, 'doc/file_forward.html', {'form':form, 'users':users})



def manager_forward(request, file_id):
    file = Document.objects.get(pk=file_id)
    users = User.objects.all()
    
    if request.method == 'POST':
        form = FileFowardForm(request.POST)

        if form.is_valid():
            forward = form.save(commit=False)
            forward.file = file 

            try:
                forward.receiver = User.objects.get(pk=int(request.POST.get('receiver', '')))
            except (ValueError, User.DoesNotExist) as e:
                return e

            forward.created_by = request.user
            forward.save()

            # call email notification method
            # -> create_notifiation_email()

            subject = f'{request.user.first_name} {request.user.last_name} Forwarded a {file.category.name}'
            from_email = settings.EMAIL_HOST_USER
            to = forward.receiver.email
            template = render_to_string('doc/email_template.html', 
                                            {'name': forward.receiver.first_name, 'category': file.category.name, 'title':file.title})
            text_content = 'You have a new message'
            msg = EmailMultiAlternatives(subject, text_content,from_email, [to])
            msg.attach_alternative(template, 'text/html')
            msg.send()

            create_notification(request, forward.receiver, 'forward', extra_id=forward.id)

            messages.success(request, f"{file.category.name} Forwarded successfuly to {forward.receiver}")

            return redirect('dashboard')
    else:
        form = FileFowardForm()
    
    return render(request, 'doc/manager_forward.html', {'form':form, 'users':users})




