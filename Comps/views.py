from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Comps.forms import ComplaintForm
from .models import Complaint


def complaint(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ComplaintForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, 'Your complaint has been registered!')
                return render(request, "complaint.html", {'form': form})
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
    complaints = Complaint.objects.all()
    return render(request, "home.html", {'complaints': complaints})


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

        return render(request, 'solvedcomplaints.html')
    else:
        messages.error(request, "You have to Login First")
        return redirect('login')


def about(request):
    return None