from django.contrib.auth.models import User

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
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), label='Department',
                                        empty_label="Choose Department",
                                        widget=forms.Select(
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

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'style': 'margin-bottom: 10px;'})
        self.fields['department'].label = 'Department'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            raise forms.ValidationError("The passwords do not match. Please try again.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Set the password
        if commit:
            user.save()
            user.department = self.cleaned_data["department"]  # Assign the selected department to the user
            user.save()
        return user


class ChangePasswordForm(forms.Form):
    CustomUser = forms.ModelChoiceField(queryset=CustomUserUser.objects.all(), empty_label="Select a user")
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        new_password = cleaned_data.get('new_password')

        # Check if the selected user exists
        if not user:
            raise forms.ValidationError("Please select a user.")

        # Check if the new password is provided
        if not new_password:
            raise forms.ValidationError("Please enter a new password.")

        return cleaned_data
