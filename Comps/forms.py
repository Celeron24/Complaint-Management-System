from django import forms
from django.contrib.auth.forms import UserCreationForm
from Comps.models import Complaint


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2')  # Customize fields as needed


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['Comp_Assign', 'complaint_type', 'Subject',  'Description']
        widgets = {
            'Comp_Assign': forms.RadioSelect(attrs={'class': 'form', 'checked': 'checked'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'Subject': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control'}),
            }
        labels = {
            'Comp_Assign': 'Is It a complaint or an option',
            'complaint_type': 'Type of Complaint',
        }
