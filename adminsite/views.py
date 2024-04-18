from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from Comps.forms import CommentForm
from Comps.models import Complaint
from .forms import ComplaintStatusUpdateForm, DepartmentForm, AddUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser and user.is_active:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized')

    return render(request, 'admin_login.html')


def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('signIn')  # Redirect to signIn page after logout


@staff_member_required
@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'dashboard.html', {'departments': departments})


def signin(request):
    return render(request, 'signIn.html', {})


@staff_member_required
@login_required
def complaint_list(request):
    users = CustomUser.objects.all()
    user = request.user
    complaints = Complaint.objects.filter(user=user)
    return render(request, 'admin/complaint_list.html', {'complaints': complaints, 'user': user, 'users': users})


@staff_member_required
@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # user_comments = complaint.comments.filter(user=complaint.user)
    # , 'user_comments': user_comments
    return render(request, 'admin/complaint_detail.html', {'complaint': complaint})


@staff_member_required
@login_required
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            # Get the user object from the form
            user = form.save(commit=False)
            # Set the hashed password using Django's built-in method
            user.set_password(form.cleaned_data['password'])
            # Assign the selected department to the user
            user.department = form.cleaned_data['department']
            user.save()
            messages.success(request, 'User added successfully')
            return redirect('dashboard')
    else:
        form = AddUserForm()
    return render(request, 'add_user.html', {'form': form})


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
@login_required
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


@staff_member_required
@login_required
def department_detail(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    users = CustomUser.objects.filter(department_id=department_id)
    return render(request, 'dept_detail.html', {'department': department, 'users': users})


@staff_member_required
@login_required
def admin_comment_submit(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.complaint = complaint
        comment.user = request.user  # Assuming the user is the admin
        comment.is_admin_comment = True
        comment.save()
        return JsonResponse({'status': 'success', 'text': comment.text,
                             'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                             })
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})


@staff_member_required
@login_required
def fetch_comments(request, complaint_id):
    # Get the complaint object
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    # Get comments related to the complaint
    comments = complaint.comments.all()
    # Render comments in a template or format as needed
    # For simplicity, let's assume comments are rendered in a template named 'comments.html'
    context = {'comments': comments}
    return render(request, 'complaint_detail.html', context)
