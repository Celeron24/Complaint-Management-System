from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Comps.forms import ComplaintForm
from .models import Complaint


def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            messages.add_message(request, messages.SUCCESS, f'Your complaint has been registered!')
            return render(request, "complaint.html", )
    else:

        form = ComplaintForm(request.POST)
    context = {'form': form, }
    return render(request, "complaint.html", context)

    # form = ComplaintForm()
    # if request.method == 'POST':
    #     form = ComplaintForm(request.POST)
    #     if form.is_valid():
    #         pass
    # return render(request, "complaint.html", {'form': form})


def home(request):
    complaints = Complaint.objects.all()
    return render(request, 'home.html', {'complaints': complaints})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, passwoord=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged IN")
            return redirect('home')
        else:
            messages.error(request, f"Invalid username or password")
            return redirect('login')
    return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('login')
