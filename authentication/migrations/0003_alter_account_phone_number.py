# Generated by Django 5.0.6 on 2024-05-09 04:47

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter a valid phone number like +12125552368', max_length=128, null=True, region=None),
        ),
    ]
