from django import forms 

from .models import Document, ForwardFile

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document', 'comment', 'category']

class FileFowardForm(forms.ModelForm):
    class Meta:
        model = ForwardFile
        fields = ['comment']