import os
import logging
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import ListView, DeleteView, UpdateView
from apps.doc.models import Document, ForwardFile, Category
from apps.doc.forms import DocumentUploadForm
from apps.userprofile.models import  ConversationMessage
from apps.core.models import User, UserType

from apps.notification.models import Notification


# config logging
#logging.basicConfig(filename='corres_update.log', filemode='w', level=logging.DEBUG)

@login_required
def dashboard(request):
    if request.user.is_authenticated and UserType.objects.get(user=request.user).is_manager:
        files = ForwardFile.objects.all()

        return render(request, 'userprofile/manager_dashboard.html', {'files':files})
    
    elif request.user.is_authenticated and UserType.objects.get(user=request.user).is_admin:

        category = request.GET.get('category')

        if category == None:
            files = Document.objects.all()
        else:
            files = Document.objects.filter(category__name=category)

        categories = Category.objects.all()

        # files = Document.objects.all()
        return render(request, 'userprofile/dashboard.html', {'categories':categories, 'files':files})

    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def manager(request):
    if request.user.is_authenticated and UserType.objects.get(user=request.user).is_manager:
        return HttpResponseRedirect(reverse('manager'))
    elif request.user.is_authenitcated and UserType.objecs.get(user=request.user).is_admin:
        return HttpResponseRedirect(reverse('dashboard'))
    
        files = ForwardFile.objects.all()
        shared = ForwardFile.objects.get(receiver=request.user.is_manager)

    return render(request, 'userprofile/manager_dashboard.html',{'files':files, 'shared':shared})


@login_required
def view_shared(request, file_id):
# TODO -> find a means to check what fikes a user can see
    # if request.user:
    #     file = get_object_or_404(ForwardFile, pk=file_id, file__created_by=request.user)
    # else:
    #     file = get_object_or_404(ForwardFile, pk=file_id, receiver=request.user)
    file = get_object_or_404(ForwardFile, pk=file_id)
    # conversation
    if request.method == 'POST':
        content  = request.POST.get('content')

        if content:
            conversationmessage = ConversationMessage.objects.create(send=file, content=content, created_by=request.user)

            return redirect('view_shared', file_id=file_id)

    return render(request, 'userprofile/view_forwarded.html', {'file':file})


@login_required

def read_notification(request):
    notifications = Notification.objects.filter(is_read=True)

    return render(request, 'userprofile/read_notification.html', {'notifications':notifications})

class UserFileListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'userprofile/user_files.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Document.objects.filter(created_by=user).order_by('-date_posted')

class FileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document
    success_url = '/dashboard'
    template_name = 'userprofile/file_confirm_delete.html'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.created_by:
            return True
        return False

# class FileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Document
#     template_name = 'userprofile/file_form.html'
#     fields = ['title', 'document', 'comment', 'category']

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

    # def test_func(self):
    #     file = self.get_object()
    #     if self.request.user == file.created_by:
    #         return True
    #     return False

@login_required()
def fileUpdate(request, file_id):
    file = Document.objects.get(pk=file_id)
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST,  files=request.FILES, instance=file)
        # if len(request.FILES) != 0: #->check if there is files in the form
        #     if len(file.document) > 0: # -> check if doc exist and remove
        #         os.remove(file.document.path)
        #     else:
        #         file.document = request.FILES['doc']
        # file.title = request.POST.get('title')
        # file.comment = request.POST.get('comment')
        # file.category = request.POST.get('category_name')
        # file.save()
        
        if form.is_valid():
            form.save()
        messages.success(request, "Document updated successfully!")
        return redirect("dashboard")
    else:
        form = DocumentUploadForm()

    return render(request, 'userprofile/update.html', {'file':file, 'form':form})

    

    # form = DocumentUploadForm(request.POST,  files=request.FILES, instance=file)

    # if form.is_valid():
    #     form.save()

    #     messages.success(request, "Document updated successfully!")
    #     return redirect("dashboard")
    
    # return render(request, 'userprofile/update.html', {'file':file})

 


# @login_required(login_url='login')
# def getFiles(request):
#     category = request.GET.get('category')

#     if category == None:
#         files = Document.objects.all()
#     else:
#         files = Document.objects.filter(category__name=category)

#     categories = Category.objects.all()
#     context = {'categories': categories, 'files':files}
#     return render(request, 'userprofile/dashboard.html', context)
