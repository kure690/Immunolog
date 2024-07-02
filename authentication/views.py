from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.utils.dateparse import parse_date
from datetime import datetime
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.contrib.auth import authenticate, login

def home(request):
    return render(request, "authentication/signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        birthday_str = request.POST['birthday']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "authentication/signup.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "authentication/signup.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "authentication/signup.html")

        try:
            birthday_date = datetime.strptime(birthday_str, "%m/%d/%Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please select a date.")
            return render(request, "authentication/signup.html")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=fname,
            last_name=lname,
            password=password1,
            birthday=birthday_date
        )

        user.save()
        login(request, user)
        return redirect('home')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return render(request, "authentication/signin.html")

        auth_user = authenticate(request, username=user.username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            messages.success(request, "Successfully logged in.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")


    return render(request, "authentication/signin.html")
    


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('signin')

@login_required
def dashboard(request):
    return render(request, "dashboard/customerdashboard.html")