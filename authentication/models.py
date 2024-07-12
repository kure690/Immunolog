from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    sex = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    civil_status = models.CharField(max_length=20, choices=[
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed')
    ], null=True, blank=True)

    def __str__(self):
        return self.username


    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
