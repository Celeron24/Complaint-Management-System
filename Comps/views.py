from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Comps.forms import ComplaintForm


def home(request):
    form = ComplaintForm()
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            pass
    return render(request, "home.html", {'form': form})


def login_user(request):
    if request.methods == "POST":
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
