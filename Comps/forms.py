from django import forms
from django.contrib.auth.forms import UserCreationForm
from Comps.models import Complaint


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'password1', 'password2')  # Customize fields as needed


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['comp_assign', 'subject', 'complaint_type', 'Description']
        widgets = {'comp_assign': forms.RadioSelect,
                   }
