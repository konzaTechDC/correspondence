from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.doc.models import Document, ForwardFile, Category
from apps.userprofile.models import  ConversationMessage
from apps.core.models import User

@login_required
def dashboard(request):
    category = request.GET.get('category')

    if category == None:
        files = Document.objects.all()
    else:
        files = Document.objects.filter(category__name=category)

    categories = Category.objects.all()
    
    # files = Document.objects.all()
    return render(request, 'userprofile/dashboard.html', {'userprofile': request.user.userprofile, 'categories':categories, 'files':files})

@login_required
def manager_dashboard(request):
    files = Document.objects.all()
    return render(request, 'userprofile/manager_dashboard.html', {'userprofile': request.user.userprofile, 'files':files})


@login_required
def view_shared(request, file_id):
    if request.userprofile.is_admin:
        file = get_object_or_404(ForwardFile, pk=file_id, document__created_by=request.user)
    else:
        file = get_object_or_404(ForwardFile, pk=file_id, created_by=request.user)

    return render(request, 'userprofile/view_forwarded.html', {'file':file})



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

class FileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Document
    template_name = 'userprofile/file_form.html'
    fields = ['title', 'document', 'comment', 'category']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.created_by:
            return True
        return False

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