from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from Comps.models import Complaint
from .forms import ComplaintStatusUpdateForm, DepartmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Department


@login_required
def dashboard(request):
    departments = Department.objects.all()
    return render(request, 'dashboard.html', {'departments': departments})


def signin(request):
    return render(request, 'signIn.html', {})


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


def add_user(request):
    return None
