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
from django.http import Http404
from django.contrib.auth import get_user_model
from records.models import VaccineRecord
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.models import Q

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
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        UserModel = get_user_model()

        superuser = authenticate(request, username=username_or_email, password=password)
        if superuser and superuser.is_superuser:
            login(request, superuser)
            return redirect('dashboard')
        
        try:
            user = UserModel.objects.get(email=username_or_email)
            auth_user = authenticate(request, username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except UserModel.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, "authentication/signin.html")
    


def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def dashboard(request):
    user = request.user
    
    if user.is_superuser:
        vaccine_records = VaccineRecord.objects.filter(Q(status='under_review') | Q(status='Under Review'))
    else:
        vaccine_records = VaccineRecord.objects.filter(user=user)
    
    context = {
        'user': user,
        'pk': user.pk,
        'vaccine_records': vaccine_records,
    }

    if user.is_superuser:
        return render(request, 'dashboard/admindashboard.html', context)
    else:
        return render(request, 'dashboard/customerdashboard.html', context)


# class InfoUpdate(LoginRequiredMixin, UpdateView):
#     model = CustomUser
#     fields = ['first_name', 'last_name', 'email', 'sex', 'address', 'birthday', 'occupation', 'civil_status', 'profile_picture']
#     template_name = 'authentication/editprofile.html'

#     def get_success_url(self):
#         return reverse_lazy('editprofile', kwargs={'pk': self.object.pk})

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         if obj != self.request.user:
#             raise Http404("You are not allowed to access this page.")
#         return obj

#     def form_valid(self, form):
#         if 'clear_profile_picture' in self.request.POST:
#             form.instance.profile_picture.delete()
#         response = super().form_valid(form)
#         if 'profile_picture' in self.request.FILES:
#             form.instance.profile_picture = self.request.FILES['profile_picture']
#             form.instance.save()
#         return response


class InfoUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'sex', 'address', 'birthday', 'occupation', 'civil_status', 'profile_picture']
    template_name = 'authentication/editprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'change_password' in request.POST:
            if password_form.is_valid():
                old_password = password_form.cleaned_data.get('old_password')
                new_password = password_form.cleaned_data.get('new_password1')
                
                try:
                    self.validate_new_password(request.user, old_password, new_password)
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password was successfully updated!', extra_tags='password')
                    return redirect(self.get_success_url())
                except ValidationError as error:
                    messages.error(request, error.message, extra_tags='password')
            else:
                for error in password_form.errors.values():
                    messages.error(request, error, extra_tags='password')
            return self.render_to_response(self.get_context_data(form=form, password_form=password_form))
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def validate_new_password(self, user, old_password, new_password):
        if not user.check_password(old_password):
            raise ValidationError("Your current password was entered incorrectly. Please enter it again.")
        
        if old_password == new_password:
            raise ValidationError("Your new password can't be the same as your current password.")
        
        # Use Django's password validators
        try:
            password_validation.validate_password(new_password, user)
        except ValidationError as error:
            raise ValidationError(error.messages[0])

    def form_valid(self, form):
        if 'clear_profile_picture' in self.request.POST:
            form.instance.profile_picture.delete()
        response = super().form_valid(form)
        if 'profile_picture' in self.request.FILES:
            form.instance.profile_picture = self.request.FILES['profile_picture']
            form.instance.save()
        messages.success(self.request, 'Your profile was successfully updated!', extra_tags='profile')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating your profile. Please check the form and try again.', extra_tags='profile')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('editprofile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404("You are not allowed to access this page.")
        return obj