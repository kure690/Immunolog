from django.contrib import admin
from django.urls import path, include
from . views import (AddVaccineRecord)

urlpatterns = [
   path('addrecord', AddVaccineRecord.as_view(), name='addrecord'),

]