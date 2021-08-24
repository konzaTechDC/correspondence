from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import DocumentUploadForm, FileFowardForm

from .models import Document, ForwardFile, Category
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
            messages.success(request, 'File Document Uploaded saved successfully.')      
            return redirect('dashboard')
    else:
        form = DocumentUploadForm()

    return render(request, 'doc/add_file.html', {'categories':categories, 'form':form})


def file_detail(request, file_id):
    # file = Document.objects.get(pk=file_id)
    file = get_object_or_404(Document, pk=file_id, created_by=request.user)

    return render(request, 'doc/file_detail.html', {'file':file})

def forward_file(request, file_id):
    file = Document.objects.get(pk=file_id)
    

    if request.method == 'POST':
        form = FileFowardForm(request.POST)

        if form.is_valid():
            forward = form.save(commit=False)
            forward.file = file 
            receiver = request.POST.get('receiver_type', 'manager')
            forward.receiver = receiver
            forward.created_by = request.user
            forward.save()

            create_notification(request, file.created_by, 'forward', extra_id=forward.id)

            messages.success(request, f"Document Forwarded successfuly to {receiver}")

            return redirect('dashboard')
    
    else:
        form = FileFowardForm()
        # messages.info(request, "Could not forward your document. Please check and resubmit")
        
    return render(request, 'doc/file_forward.html', {'form':form})
    
