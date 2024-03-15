from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from Comps.forms import ComplaintForm
from .models import Complaint
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def your_search_view(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            # Ensure that only complaints belonging to the current user are retrieved
            searched_complaints = Complaint.objects.filter(
                Q(id__icontains=query) |
                Q(Comp_Assign__icontains=query) |
                Q(Subject__icontains=query),
                user=request.user
            )
        else:
            # Also filter complaints by the current user
            searched_complaints = Complaint.objects.filter(user=request.user)
        return render(request, 'search.html', {'searched_complaints': searched_complaints})
    else:
        # Handle the case where the user is not authenticated (optional)
        return render(request, 'login.html')


def complaint(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ComplaintForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user  # Ensure the complaint is associated with the current user
                instance.save()
                messages.success(request, 'Your complaint has been registered!')
                return redirect('home')  # Redirect to the homepage after submitting the form
        else:
            form = ComplaintForm()
        context = {'form': form}
        return render(request, "complaint.html", context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login.html')


def home(request):
    if request.user.is_authenticated:
        default_sort_field = '-status'

        sort_by = request.GET.get('sort_by', default_sort_field)

        if sort_by == '-status':
            all_complaints = Complaint.objects.filter(user=request.user).order_by('-status', 'created_at')
        else:
            all_complaints = Complaint.objects.filter(user=request.user).order_by(sort_by)

        paginator = Paginator(all_complaints, 5)
        page = request.GET.get('page')

        try:
            all_complaints = paginator.page(page)
        except PageNotAnInteger:
            all_complaints = paginator.page(1)
        except EmptyPage:
            all_complaints = paginator.page(paginator.num_pages)

        context = {'all_complaints': all_complaints, 'sort_by': sort_by}
        return render(request, 'home.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged IN")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('login')


def solvedcomplaints(request):
    if request.user.is_authenticated:
        solved_complaints = Complaint.objects.filter(status=1, user=request.user)
        return render(request, 'solvedcomplaints.html', {'solved_complaints': solved_complaints})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')


def about(request):
    return None


class ViewComplaint(DetailView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'view_complaint.html'
    context_object_name = 'complaint'  # Optionally specify the context variable name

    def get_object(self, queryset=None):
        return Complaint.objects.get(pk=self.kwargs['pk'], user=self.request.user)
