from django.contrib import admin
from django.urls import path, include
from .views import AddVaccineRecord, AcceptedVaccineRecord, RejectedVaccineRecord
from .views import accept_vaccine_record, reject_vaccine_record

urlpatterns = [
   path('addrecord', AddVaccineRecord.as_view(), name='addrecord'),
   path('accept_vaccine_record/<int:pk>/', accept_vaccine_record, name='accept_vaccine_record'),
   path('reject_vaccine_record/<int:pk>/', reject_vaccine_record, name='reject_vaccine_record'),
   path('verified', AcceptedVaccineRecord.as_view(), name='verified'),
   path('rejected', RejectedVaccineRecord.as_view(), name='rejected'),

]