# Generated by Django 3.2.3 on 2021-06-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210611_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentrecord',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookappointment',
            name='appointment_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]