# Generated by Django 3.2.3 on 2021-06-11 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_bookappointment_symptoms'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookappointment',
            name='doctor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookappointment',
            name='hospital',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]