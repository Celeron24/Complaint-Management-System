from Comps.models import Complaint
from django import forms
from .models import Department


class ComplaintStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type Department name',
                                           'style': 'margin-bottom: 10px;'}),
        }
