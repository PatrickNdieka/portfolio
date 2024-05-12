# Generated by Django 5.0.6 on 2024-05-09 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0010_alter_configurationsetting_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configurationsetting',
            name='value',
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='file_value',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='image_value',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='integer_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='text_value',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='url_value',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configurationsetting',
            name='value_type',
            field=models.CharField(choices=[('text', 'Text'), ('integer', 'Integer'), ('url', 'URL'), ('image', 'Image'), ('file', 'File')], default='text', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='configurationsetting',
            name='key',
            field=models.CharField(max_length=255),
        ),
    ]