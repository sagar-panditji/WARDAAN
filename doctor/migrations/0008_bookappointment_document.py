# Generated by Django 3.1.1 on 2021-07-06 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0007_bookappointment_doctor_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookappointment',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
