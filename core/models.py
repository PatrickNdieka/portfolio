from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from tinymce import models as tinymce_models

User = get_user_model()


class StatusChoices(models.IntegerChoices):
    DRAFT = (0, _('Draft'))
    PUBLISHED = (1, _('Published'))


class ProjectPortfolio(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    description = tinymce_models.HTMLField()
    content = tinymce_models.HTMLField()
    featured_image = models.ImageField(upload_to='projects/featured/')
    featured = models.BooleanField(
        verbose_name='Featured project', default=False)
    status = models.IntegerField(
        choices=StatusChoices, default=StatusChoices.DRAFT)
    published_on = models.DateField(verbose_name='Publish date')
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='author')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(verbose_name='Skill', max_length=150)
    projects = models.ManyToManyField(
        'ProjectPortfolio', related_name='skills')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
