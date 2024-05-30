from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('portfolio/', views.ProjectListView.as_view(), name='portfolio'),
    path('portfolio/project/<slug:slug>/', views.ProjectDetailView.as_view(),
         name='portfolio_project_detail'),
    path('consent_message/', views.consent_message, name='consent_message'),
    path('subscribe/', views.SubscriptionCreateView.as_view(), name='subscribe'),
    path('verify-email/<str:token>/',
         views.VerifySubscriberEmailView.as_view(), name='verify_email'),
    path('subscription_success/', views.TemplateView.as_view(
        template_name="subscription_success.html"), name='subscription_success'),
]
