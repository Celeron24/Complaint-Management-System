from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from Comps.models import Complaint
from .forms import ComplaintStatusUpdateForm, DepartmentForm
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
            return redirect('dashboard')  # Redirect to admin dashboard or any other admin page
        else:
            messages.error(request, 'Invalid credentials or not authorized')

    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('signIn')  # Redirect to admin login page after logout


@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'dashboard.html', {'departments': departments})


def signin(request):
    return render(request, 'signIn.html', {})


@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        designation = request.POST['designation']
        name = request.POST['name']
        if not CustomUser.objects.filter(username=username).exists():
            CustomUser.objects.create_user(username=username, password=password, designation=designation, name=name)
            messages.success(request, 'User added successfully')
        else:
            messages.error(request, 'Username already exists')

        return redirect('user_management')

    return render(request, 'add_user.html')  # Create a new HTML template for adding users


@login_required
def user_management(request):
    users = CustomUser.objects.all()

    if request.method == 'POST':
        if 'add_user' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            designation = request.POST['designation']
            name = request.POST['name']
            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create_user(username=username, password=password, designation=designation,
                                         name=name,
                                         )
                messages.success(request, 'User added successfully')
            else:
                messages.error(request, 'Username already exists')

        elif 'update_user' in request.POST:
            user_id = request.POST['user_id']
            username = request.POST['username']
            password = request.POST['password']
            designation = request.POST['designation']
            name = request.POST['name']
            user = User.objects.get(pk=user_id)
            user.username = username
            user.set_password(password)
            user.designation = designation
            user.name = name
            user.save()
            messages.success(request, 'User updated successfully')

        elif 'delete_user' in request.POST:
            user_id = request.POST['delete_user']
            user = CustomUser.objects.get(pk=user_id)
            if user.is_superuser:
                messages.error(request, 'Cannot delete superuser')
            else:
                user.delete()
                messages.success(request, 'User deleted successfully')

        return redirect('user_management')

    return render(request, 'user_management.html', {'users': users})


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


@login_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            messages.success(request, f'Department with name "{name}" has been added.')
            return redirect('dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'add_department.html', {'form': form})
