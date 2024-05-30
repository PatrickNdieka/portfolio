import hashlib
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .models import (
    SectionInformation, Service, ProjectPortfolio, StatusChoices, ValueType, Subscription
)

from .forms import SubscriptionForm


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
            'about_location': about_details.filter(title__icontains='location', value_type=ValueType.HTML).first(),
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


class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'core/partials/subscription_success.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.send_verification_email(self.request)
        print(self.object)
        return render(self.request, self.template_name, {
            'full_name': self.object.full_name,
            'email': self.object.email,
        })

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class VerifySubscriberEmailView(TemplateView):
    template_name = 'verify_email.html'

    def get(self, request, token, *args, **kwargs):
        signer = TimestampSigner()
        try:
            signed_pk = signer.unsign(token, max_age=604800)
            pk = force_str(urlsafe_base64_decode(signed_pk))
            subscription = get_object_or_404(Subscription, pk=pk)
        except (SignatureExpired, BadSignature, TypeError, ValueError, OverflowError, Subscription.DoesNotExist):
            subscription = None

        if subscription is not None and not subscription.is_verified:
            subscription.is_verified = True
            subscription.save()
            return render(request, 'core/email_verification_success.html')
        else:
            return render(request, 'core/email_verification_failed.html')


def consent_message(request):
    return render(request, 'core/partials/consent_message_partial.html')
