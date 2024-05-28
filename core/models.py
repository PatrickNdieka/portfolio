import os
import nbformat
from nbconvert import HTMLExporter
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from tinymce import models as tinymce_models

User = get_user_model()


class StatusChoices(models.IntegerChoices):
    DRAFT = (0, _('Draft'))
    PUBLISHED = (1, _('Published'))


class ContentType(models.TextChoices):
    HTML = 'html', ('HTML')
    NOTEBOOK = 'notebook', _('Jupyter Notebook')
    PDF = 'pdf', _('PDF')


class ProjectPortfolio(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = tinymce_models.HTMLField()
    content_type = models.CharField(
        max_length=20, choices=ContentType.choices, default=ContentType.HTML)
    content = tinymce_models.HTMLField(null=True, blank=True)
    file = models.FileField(upload_to='files/projects', null=True, blank=True)
    featured_image = models.ImageField(upload_to='images/projects/featured/')
    featured = models.BooleanField(
        verbose_name='Featured project', default=False)
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    published_on = models.DateField(verbose_name='Publish date')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-published_on', 'title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:portfolio_project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.content_type == ContentType.NOTEBOOK:
            self.content = self.convert_notebook_to_html()
        super().save(*args, **kwargs)

    def convert_notebook_to_html(self):
        file_content = self.file.read()
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        try:
            notebook_node = nbformat.reads(file_content, as_version=4)
        except Exception as e:
            raise ValueError(f"Error reading notebook content: {e}")
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(notebook_node)

        return body


class Skill(models.Model):
    name = models.CharField(verbose_name='Skill', max_length=150)
    image = models.ImageField(upload_to='images/skills/', null=True)
    projects = models.ManyToManyField(
        'ProjectPortfolio', related_name='skills')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(
        verbose_name='Service', max_length=100, unique=True)
    description = tinymce_models.HTMLField()
    projects = models.ManyToManyField(
        'ProjectPortfolio', related_name='services')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ValueType(models.TextChoices):
    TEXT = 'text', 'Text'
    HTML = 'html', 'HTML'
    EMAIL = 'email', 'Email'
    PHONE = 'phone', 'Phone number'
    URL = 'url', 'URL'
    IMAGE = 'image', 'Image'
    FILE = 'file', 'File'


class ConfigurationSetting(models.Model):
    key = models.CharField(max_length=50)
    value_type = models.CharField(
        max_length=10, choices=ValueType.choices, default=ValueType.TEXT)
    text_value = models.CharField(max_length=100, blank=True, null=True)
    html_value = tinymce_models.HTMLField(blank=True, null=True)
    email_value = models.EmailField(blank=True, null=True)
    phone_value = PhoneNumberField(
        help_text='Enter a valid phone number like +12125552368',
        blank=True, null=True)
    url_value = models.URLField(blank=True, null=True)
    image_value = models.ImageField(upload_to='images/', blank=True, null=True)
    file_value = models.FileField(upload_to='files/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True,
        blank=True, related_name='children')

    def __str__(self):
        if self.parent:
            return f'{self.parent}_{self.key}'
        return self.key

    @property
    def get_value(self):
        field_name = f"{self.value_type}_value"
        return getattr(self, field_name, None)


class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True,
        blank=True, related_name='sub_sections')

    def __str__(self):
        if self.parent:
            return f'{self.parent} | {self.name}'
        return self.name


class SectionInformation(models.Model):
    SECTION_VALUE_CHOICES = [
        (value, label) for value, label in ValueType.choices if value in [ValueType.IMAGE, ValueType.HTML]
    ]
    section = models.ForeignKey(
        'Section', on_delete=models.CASCADE, related_name='information')
    title = models.CharField(max_length=50, unique=True)
    value_type = models.CharField(
        max_length=10, choices=SECTION_VALUE_CHOICES, default=ValueType.HTML)
    html_value = tinymce_models.HTMLField(blank=True, null=True)
    image_value = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def get_value(self):
        field_name = f"{self.value_type}_value"
        return getattr(self, field_name, None)
