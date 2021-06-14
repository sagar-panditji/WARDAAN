# Generated by Django 3.2.3 on 2021-06-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_doctor_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='hospital',
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic_close_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic_open_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]