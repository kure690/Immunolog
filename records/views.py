from django.shortcuts import render, redirect
from django.views import View
from .models import VaccineRecord
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


# class AddVaccineRecord(LoginRequiredMixin, CreateView):

#     def test_func(self):
#         return self.request.user.is_superuser
    

#     model = VaccineRecord
#     fields = ['vaccination_date', 'vaccine_type', 'attending_physician_first_name', 'attending_physician_last_name', 'vaccine_venue', 'proof_document']
#     success_url = reverse_lazy('dashboard')
#     template_name = 'records/add_record.html'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import VaccineRecordForm
from .models import VaccineRecord

class AddVaccineRecord(LoginRequiredMixin, CreateView):
    form_class = VaccineRecordForm
    success_url = reverse_lazy('dashboard')
    template_name = 'records/add_record.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.request.user.pk
        return context

    def test_func(self):
        return self.request.user.is_superuser

    

@login_required
def accept_vaccine_record(request, pk):
    record = get_object_or_404(VaccineRecord, pk=pk)
    record.status = 'Verified'
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
    if request.method == 'POST':
        record = get_object_or_404(VaccineRecord, pk=pk)
        rejection_reason = request.POST.get('rejection_reason')
        
        record.status = 'Rejected'
        record.rejection_reason = rejection_reason
        record.save()
        
        return redirect('dashboard')
    
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
    template_name = 'records/rejectedrecords.html'

    def get_queryset(self):
        return VaccineRecord.objects.filter(status='Rejected')

    def test_func(self):
        return self.request.user.is_superuser
    
    def test_func(self):
        return self.request.user.is_authenticated 

@login_required
def delete_vaccine_record(request, pk):
    record = get_object_or_404(VaccineRecord, pk=pk)
    return redirect('dashboard')

@login_required
@require_http_methods(["GET", "POST"])
def edit_vaccine_record(request, pk):
    record = get_object_or_404(VaccineRecord, pk=pk, user=request.user)
    
    if request.method == 'GET':
        data = {
            'id': record.id,
            'vaccination_date': record.vaccination_date,
            'vaccine_type': record.vaccine_type,
            'attending_physician_first_name': record.attending_physician_first_name,
            'attending_physician_last_name': record.attending_physician_last_name,
            'vaccine_venue': record.vaccine_venue,
            'proof_document': record.proof_document.url if record.proof_document else '',
        }
        return JsonResponse(data, encoder=DjangoJSONEncoder)
    
    elif request.method == 'POST':
        record.vaccination_date = request.POST.get('vaccination_date')
        record.vaccine_type = request.POST.get('vaccine_type')
        record.attending_physician_first_name = request.POST.get('attending_physician_first_name')
        record.attending_physician_last_name = request.POST.get('attending_physician_last_name')
        record.vaccine_venue = request.POST.get('vaccine_venue')
        
        if 'proof_document' in request.FILES:
            record.proof_document = request.FILES['proof_document']
        
        record.save()
        return JsonResponse({'status': 'success'})