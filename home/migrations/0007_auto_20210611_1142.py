# Generated by Django 3.2.3 on 2021-06-11 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210611_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookappointment',
            old_name='doctor',
            new_name='doctor_id',
        ),
        migrations.RenameField(
            model_name='bookappointment',
            old_name='hospital',
            new_name='hospital_id',
        ),
        migrations.RenameField(
            model_name='bookappointment',
            old_name='patient',
            new_name='patient_id',
        ),
    ]