from Comps.models import Complaint
from django import forms
from .models import Department, CustomUser


class UserManagementForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'designation']  # Include other fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['name'].required = False
        self.fields['designation'].required = False


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


class AddUserForm(forms.ModelForm):
    password_confirmation = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'designation', 'name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a unique username',
                                               'style': 'margin-bottom: 10px;'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your rank',
                                                  'style': 'margin-bottom: 10px;'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your full name',
                                           'style': 'margin-bottom: 10px;'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("The passwords do not match. Please try again.")
        return cleaned_data
