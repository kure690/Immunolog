from django.shortcuts import render, redirect
from django.views import View
from .models import VaccineRecord
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

class AddVaccineRecord(LoginRequiredMixin, CreateView):
    model = VaccineRecord
    fields = ['vaccination_date', 'vaccine_type', 'attending_physician_first_name', 'attending_physician_last_name', 'vaccine_venue', 'proof_document']
    success_url = reverse_lazy('dashboard')
    template_name = 'records/add_record.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

@login_required
def accept_vaccine_record(request, pk):
    record = get_object_or_404(VaccineRecord, pk=pk)
    record.status = 'verified'
    record.save()
    return redirect('dashboard')

class UserVaccineRecord(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VaccineRecord
    context_object_name = 'vaccine_records'
    template_name = 'dashboard/customerdashboard.html'

    def get_queryset(self):
        return VaccineRecord.objects.filter(user=self.request.user)

    def test_func(self):
        return self.request.user.is_not_superuser
    
    def test_func(self):
        return self.request.user.is_authenticated
    
@login_required
def reject_vaccine_record(request, pk):
    record = get_object_or_404(VaccineRecord, pk=pk)
    record.status = 'Rejected'
    record.save()
    return redirect('dashboard')

class AcceptedVaccineRecord(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VaccineRecord
    context_object_name = 'vaccine_records'
    template_name = 'records/acceptedrecords.html'

    def get_queryset(self):
        return VaccineRecord.objects.filter(status='Verified')

    def test_func(self):
        return self.request.user.is_superuser
    
    def test_func(self):
        return self.request.user.is_authenticated 
    
class RejectedVaccineRecord(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VaccineRecord
    context_object_name = 'vaccine_records'
    template_name = 'records/acceptedrecords.html'

    def get_queryset(self):
        return VaccineRecord.objects.filter(status='Rejected')

    def test_func(self):
        return self.request.user.is_superuser
    
    def test_func(self):
        return self.request.user.is_authenticated 