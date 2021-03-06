# Generated by Django 3.1.1 on 2021-06-28 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210628_0832'),
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('appointment_date', models.DateField(auto_now_add=True, null=True)),
                ('appointment_time', models.TimeField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Confirmed'), (0, 'Waiting'), (-1, 'Cancelled')], default=0, null=True)),
                ('patient_id', models.IntegerField(blank=True, null=True)),
                ('doctor_id', models.IntegerField(blank=True, null=True)),
                ('fees_submitted', models.IntegerField(blank=True, default=0, null=True)),
                ('symptoms', models.ManyToManyField(to='home.Symptom')),
            ],
        ),
    ]
