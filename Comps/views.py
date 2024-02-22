from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def home(request):
    return render(request, "home.html")


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
    messages.success("You have successfully logged out")
    return redirect('login')
