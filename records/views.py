from django.shortcuts import render, redirect
from django.views import View
from .models import VaccineRecord
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy

class AddVaccineRecord(LoginRequiredMixin, CreateView):
    model = VaccineRecord
    fields = ['vaccination_date', 'vaccine_type', 'attending_physician_first_name', 'attending_physician_last_name', 'vaccine_venue', 'proof_document']
    success_url = reverse_lazy('dashboard')
    template_name = 'records/add_record.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)