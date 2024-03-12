from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from Comps.forms import ComplaintForm
from .models import Complaint
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max, Min


def your_search_view(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            searched_complaints = Complaint.objects.filter(
                Q(id__icontains=query) |
                Q(Comp_Assign__icontains=query) |
                Q(Subject__icontains=query)
            )
        else:
            searched_complaints = Complaint.objects.all()

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
                instance.user = request.user
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

    # form = ComplaintForm()
    # if request.method == 'POST':
    #     form = ComplaintForm(request.POST)
    #     if form.is_valid():
    #         pass
    # return render(request, "complaint.html", {'form': form})


def home(request):
    valid_sort_fields = ['id', 'Subject', 'created_at']
    default_sort_field = 'created_at'

    sort_by = request.GET.get('sort_by', default_sort_field)

    if sort_by not in valid_sort_fields:
        sort_by = default_sort_field

    # Determine the appropriate order based on sort_by
    order = sort_by if not sort_by.endswith('-') else f'-{sort_by.rstrip("-")}'

    # Use aggregation to get the min and max created_at values
    min_created_at = Complaint.objects.all().aggregate(min_created_at=Min('created_at'))['min_created_at']
    max_created_at = Complaint.objects.all().aggregate(max_created_at=Max('created_at'))['max_created_at']

    # Determine the oldest and latest created_at values
    oldest_created_at = min_created_at if sort_by == 'created_at' else None
    latest_created_at = max_created_at if sort_by == 'created_at' else None

    all_complaints = Complaint.objects.all().order_by(order)
    paginator = Paginator(all_complaints, 5)

    page = request.GET.get('page')
    try:
        all_complaints = paginator.page(page)
    except PageNotAnInteger:
        all_complaints = paginator.page(1)
    except EmptyPage:
        all_complaints = paginator.page(paginator.num_pages)

    context = {
        'all_complaints': all_complaints,
        'sort_by': sort_by,
        'oldest_created_at': oldest_created_at,
        'latest_created_at': latest_created_at,
    }
    return render(request, 'home.html', context)


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


# def search(request):
#     if request.method == "POST":
#         # Grab the form field input
#         search = request.POST['search']
#         # Search the database
#         searched = Meep.objects.filter(body__contains=search)
#
#         return render(request, 'search.html', {'search': search, 'searched': searched})
#     else:
#         return render(request, 'search.html', {})
def solvedcomplaints(request):
    if request.user.is_authenticated:
        solved_complaints = Complaint.objects.filter(status=2)
        return render(request, 'solvedcomplaints.html', {'solved_complaints': solved_complaints})
    else:
        messages.error(request, "You have to Login First")
        return redirect('login')


def about(request):
    return None


class ViewComplaint(DetailView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'view_complaint.html'
    context_object_name = 'complaint'  # Optionally specify the context variable name

    def get_object(self, queryset=None):
        return Complaint.objects.get(pk=self.kwargs['pk'])
