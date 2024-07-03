from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class VaccineRecord(models.Model):
    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('under_review', 'Under Review'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')
    vaccination_date = models.DateField()
    submission_date = models.DateTimeField(auto_now_add=True)
    vaccine_type = models.CharField(max_length=100)
    proof_document = models.ImageField(upload_to='vaccine_pics/')
    attending_physician_first_name = models.CharField(max_length=100, default='John')
    attending_physician_last_name = models.CharField(max_length=100, default='Doe')
    vaccine_venue = models.CharField(max_length=100, default='Johnson & Johnson')
    
    def __str__(self):
        return f"{self.user.username} - {self.vaccine_type} on {self.vaccination_date}"
    
