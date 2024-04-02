from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from Comps.models import Complaint, Comment
from .models import ComplaintType


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')  # Customize fields as needed


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['Comp_Assign',  'complaint_type', 'Subject', 'Description']
        complaint_type = forms.ModelChoiceField(queryset=ComplaintType.objects.all(), empty_label=None)
        widgets = {
            'Comp_Assign': forms.RadioSelect(attrs={'class': 'form', 'checked': 'checked',
                                                    'style': 'margin-bottom: 10px;'}),

            'complaint_type': forms.Select(attrs={'class': 'form-control'}),

            'Subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write the subject here',
                                              'style': 'margin-bottom: 10px;'}),

            'Description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here',
                                                 'style': 'margin-bottom: 10px;'}),
        }

        labels = {
            'Comp_Assign': 'Choose Type:',
            'Subject': 'Subject (Max 50 character):',
            'complaint_type': 'Type of Complaint',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['Comp_Assign'].required = True
        self.fields['complaint_type'].required = True
        self.fields['Subject'].required = True
        self.fields['Description'].required = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
        }
