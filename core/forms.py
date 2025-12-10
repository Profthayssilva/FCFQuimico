from django import forms
from .models import DownloadRequest, Document

class DownloadRequestForm(forms.ModelForm):
    class Meta:
        model = DownloadRequest
        fields = ['name', 'role', 'company', 'contact', 'document']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Seu nome'}),
            'role': forms.TextInput(attrs={'placeholder': 'Seu cargo'}),
            'company': forms.TextInput(attrs={'placeholder': 'Empresa'}),
            'contact': forms.TextInput(attrs={'placeholder': 'WhatsApp ou e-mail'}),
        }
