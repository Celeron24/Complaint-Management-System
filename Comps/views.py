from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from Comps.forms import ComplaintForm, CommentForm
from .models import Complaint
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def your_search_view(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            # Ensure that only complaints belonging to the current user are retrieved
            searched_complaints = Complaint.objects.filter(
                Q(id__iexact=query) |
                Q(Comp_Assign__iexact=query) |
                Q(Subject__iexact=query),
                user=request.user
            )
        else:
            searched_complaints = Complaint.objects.none()
            messages.error(request, 'Type either the ID or Subject of complaint/assignment')
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
            all_complaints = Complaint.objects.filter(user=request.user).order_by('-status', '-created_at')
        else:
            all_complaints = Complaint.objects.filter(user=request.user).order_by(sort_by)

        paginator = Paginator(all_complaints, 10)
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
    return render(request, 'about.html')


# def view_complaint(request, complaint_id):
#     if request.user.is_authenticated:
#         complaint_view = get_object_or_404(Complaint, id=complaint_id)
#
#         # Check if the logged-in user is the same as the user who submitted the complaint
#         if request.user.username == complaint_view.user.username:
#             return render(request, 'view_complaint.html', {'complaint_view': complaint_view})
#         else:
#             # If the logged-in user is not the same as the user who submitted the complaint, handle accordingly
#             messages.error(request, "You are not authorized to view this complaint.")
#             return redirect('home')  # Redirect to a suitable page, like the dashboard
#     else:
#         messages.error(request, "You have to log in first")
#         return redirect('login')

def view_complaint(request, pk):
    if request.user.is_authenticated:
        try:
            complaint = Complaint.objects.get(id=pk)
            if request.user.is_staff:  # Check if the user is an admin
                comments = complaint.comments.filter(is_admin_comment=True)
            else:
                comments = complaint.comments.all()
        except Complaint.DoesNotExist:
            messages.error(request, "The complaint you are trying to view does not exist.")
            return redirect('home')  # Redirect the user to the home page or any other page

        form = CommentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.complaint = complaint
                new_comment.user = request.user
                if request.user.is_staff:  # Set is_admin_comment field for admin comments
                    new_comment.is_admin_comment = True
                new_comment.save()
                form = CommentForm()  # Reset form after saving comment

        context = {
            'complaint': complaint,
            'comments': comments,  # Pass comments to the template context
            'form': form,
        }
        return render(request, 'view_complaint.html', context)
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')
