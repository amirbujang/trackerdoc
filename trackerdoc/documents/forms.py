from django import forms

from .models import Data, Document, State, Template, TemplateTag

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'note', 'current_state']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Filename'
        }
        help_texts = {
            'name': 'Name will be used for PDF file download'
        }

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['content', 'template_tag']
        widgets = {
            'template_tag': forms.HiddenInput(),
            'content': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class TemplateUploadForm(forms.ModelForm):
    html_template = forms.FileField()

    class Meta:
        model = Template
        fields = ['name', 'description', 'html_template', 'is_active',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'description', 'template_single_page', 'filename_tag', 'is_active']
        label = {
            'template_single_page': 'Html Template',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'template_single_page': forms.Textarea(attrs={'rows': 3}),
        }

class TemplateTagForm(forms.ModelForm):
    class Meta:
        model = TemplateTag
        fields = ['tag', 'label', 'type', 'default_content', 'is_capitalize', 'is_autocomplete', 'is_searchable']
        label = {
            'tag': 'Field',
        }
        widgets = {
            'default_content': forms.TextInput(),
        }

class ReportForm(forms.Form):
    type_choice = [
        ('yearly', 'Yearly',),
        ('monthly', 'Monthly'),
        # ('daily', 'Daily'),
    ]

    year_choice = [
        (2018, '2018'),
    ]

    month_choice = [
        (1, 'January'),
        (2, 'Febuary'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ]

    states = State.objects.all()
    state_choice = [(state.id, state.name) for state in states]

    report_type = forms.ChoiceField(choices=type_choice)
    year = forms.ChoiceField(choices=year_choice)
    month = forms.ChoiceField(choices=month_choice)
    status = forms.ChoiceField(choices=state_choice)

class StatusUpdateForm(forms.Form):
    document_id = forms.IntegerField()
    destination_id = forms.IntegerField()
