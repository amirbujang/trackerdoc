from django import forms

from .models import Data

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'note', 'current_state']
        

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['content', 'template_tag']
        widgets = {
            'template_tag': forms.HiddenInput(),
            'content': forms.TextInput(),
        }
