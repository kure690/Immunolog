# Generated by Django 5.0.6 on 2024-07-03 03:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('verified', 'Verified'), ('under_review', 'Under Review'), ('rejected', 'Rejected')], default='under_review', max_length=20)),
                ('vaccination_date', models.DateField()),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('vaccine_type', models.CharField(max_length=100)),
                ('proof_document', models.ImageField(upload_to='vaccine_pics/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
