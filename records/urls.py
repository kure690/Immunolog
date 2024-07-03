from django.contrib import admin
from django.urls import path, include
from .views import (AddVaccineRecord)
from .views import accept_vaccine_record

urlpatterns = [
   path('addrecord', AddVaccineRecord.as_view(), name='addrecord'),
   path('accept_vaccine_record/<int:pk>/', accept_vaccine_record, name='accept_vaccine_record'),

]