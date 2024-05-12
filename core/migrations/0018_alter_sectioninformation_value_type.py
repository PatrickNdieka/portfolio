# Generated by Django 5.0.6 on 2024-05-10 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_configurationsetting_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectioninformation',
            name='value_type',
            field=models.CharField(choices=[('html', 'HTML'), ('image', 'Image')], default='html', max_length=10),
        ),
    ]