from django.shortcuts import render
from django.db.models import Case, When, F, Value, CharField, Q
from django.views.generic import TemplateView

from .models import Section, SectionInformation, Service


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.filter(featured=True)
        about_details = SectionInformation.objects.select_related(
            'section').filter(section__name__icontains='about')

        about_details = {
            'about_image': about_details.filter(title__icontains='image').first(),
            'about_content': about_details.filter(title__icontains='content').first(),
        }
        context.update(
            about_details=about_details,
            services=services
        )
        return context
