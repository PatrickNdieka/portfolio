from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Section, SectionInformation, Service, ProjectPortfolio, StatusChoices, ValueType


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.filter(featured=True)
        about_details = SectionInformation.objects.select_related(
            'section').filter(section__name__icontains='about')

        about_details = {
            'about_image': about_details.filter(title__icontains='image', value_type=ValueType.IMAGE).first(),
            'about_content': about_details.filter(title__icontains='content', value_type=ValueType.HTML).first(),
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(featured=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_project = self.queryset.filter(featured=True)
        if featured_project:
            context.update({
                'featured_project': featured_project.get(),
            })
        return context


class ProjectDetailView(DetailView):
    template_name = 'core/project_detail.html'
    model = ProjectPortfolio
    context_object_name = 'project'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_image = SectionInformation.objects.select_related(
            'section').filter(
                section__name__icontains='about',
                title__icontains='image',
                value_type=ValueType.IMAGE)
        if about_image:
            context.update({'about_image': about_image.first()})
        return context


def consent_message(request):
    return render(request, 'core/partials/consent_message_partial.html')
