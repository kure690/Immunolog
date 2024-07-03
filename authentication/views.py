from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
from django.utils.dateparse import parse_date
from datetime import datetime
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.

from django.contrib.auth import authenticate, login

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        sex = request.POST['sex']
        birthday_str = request.POST['birthday']
        address = request.POST['address']
        occupation = request.POST['occupation']
        civil_status = request.POST['civil_status']
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
            birthday=birthday_date,
            sex = sex,
            address = address,
            occupation = occupation,
            civil_status = civil_status
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
    user = request.user
    context = {
        'user': user,
        'pk': user.pk  # Ensure pk is passed to the context
    }
    return render(request, 'dashboard/customerdashboard.html', context)

class InfoUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'sex', 'address', 'birthday', 'occupation', 'civil_status', 'profile_picture']
    template_name = 'authentication/editprofile.html'

    def get_success_url(self):
        return reverse_lazy('editprofile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404("You are not allowed to access this page.")
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        if 'profile_picture' in self.request.FILES:
            form.instance.profile_picture = self.request.FILES['profile_picture']
            form.instance.save()
        return response