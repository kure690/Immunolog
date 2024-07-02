from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('signin', views.signin_user, name='signin'),
   path('signin', views.signin_admin, name='signin'),
   path('signup', views.signup, name='signup'),
   path('signout', views.signout, name='signout'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('reset_password/', auth_views.PasswordResetView.as_view(template_name='authentication/resetpass.html'), name = "reset_password"),
   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/resetsent.html'), name = "password_reset_done"),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/resetconfirmation.html'), name = "password_reset_confirm"),
   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/resetcomplete.html'), name = "password_reset_complete"),
]