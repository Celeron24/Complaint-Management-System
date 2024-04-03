from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from Comps.models import Complaint
from .forms import ComplaintStatusUpdateForm, DepartmentForm, AddUserForm, UserManagementForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized')

    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('admin_login')  # Redirect to admin login page after logout


@staff_member_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'dashboard.html', {'departments': departments})


def signin(request):
    return render(request, 'signIn.html', {})


@staff_member_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully')
            return redirect('user_management')
    else:
        form = AddUserForm()
    return render(request, 'add_user.html', {'form': form})


@login_required
def user_management(request):
    users = CustomUser.objects.all()
    form = UserManagementForm()  # Instantiate the form

    if request.method == 'POST':
        form = UserManagementForm(request.POST)
        if form.is_valid():  # Check if the form is valid
            action = form.cleaned_data.get('action')
            user_id = form.cleaned_data.get('user_id')

            if action == 'update':
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                designation = form.cleaned_data.get('designation')
                name = form.cleaned_data.get('name')
                user = CustomUser.objects.get(pk=user_id)
                user.username = username
                user.set_password(password)
                user.designation = designation
                user.name = name
                user.save()
                messages.success(request, 'User updated successfully')

            elif action == 'delete':
                user = CustomUser.objects.get(pk=user_id)
                if not user.is_superuser:
                    user.delete()
                    messages.success(request, 'User deleted successfully')
                else:
                    messages.error(request, 'Cannot delete superuser')

            return redirect('user_management')

    return render(request, 'user_management.html', {'users': users, 'form': form})


@method_decorator(login_required, name='dispatch')
class ComplaintDetailView(View):
    def get(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        form = ComplaintStatusUpdateForm(instance=complaint)
        return render(request, 'complaint_detail.html', {'complaint': complaint, 'form': form})

    def post(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        form = ComplaintStatusUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_detail', pk=pk)
        return render(request, 'complaint_detail.html', {'complaint': complaint, 'form': form})


@staff_member_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully')
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})
