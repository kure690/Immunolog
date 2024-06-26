from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.utils.dateparse import parse_date
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        birthday_str = request.POST['birthday']
        email = request.POST['email']
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
            first_name=fname,
            last_name=lname,
            email=email,
            password=password1,
            birthday=birthday_date
        )

        user.save()
        login(request, user)
        return redirect('home')

    return render(request, "authentication/signup.html")


def signin(request):
    return render(request, "authentication/signin.html")

def signout(request):
    return render(request, "authentication/index.html")