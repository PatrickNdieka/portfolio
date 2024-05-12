from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Section, SectionInformation, Service, ProjectPortfolio, StatusChoices


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


class ProjectListView(ListView):
    template_name = 'core/projects_list.html'
    queryset = ProjectPortfolio.objects.prefetch_related(
        'skills').filter(status=StatusChoices.PUBLISHED)
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    template_name = 'core/project_detail.html'
    model = ProjectPortfolio
    context_object_name = 'project'
    query_pk_and_slug = True
