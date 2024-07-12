from django import forms
from .models import VaccineRecord

class VaccineRecordForm(forms.ModelForm):
    class Meta:
        model = VaccineRecord
        fields = ['vaccination_date', 'vaccine_type', 'attending_physician_first_name', 'attending_physician_last_name', 'vaccine_venue', 'proof_document']

    def __init__(self, *args, **kwargs):
        super(VaccineRecordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
