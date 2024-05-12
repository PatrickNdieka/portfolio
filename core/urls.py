from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('portfolio/', views.ProjectListView.as_view(), name='portfolio'),
    path('portfolio/project/<slug:slug>/', views.ProjectDetailView.as_view(),
         name='portfolio_project_detail'),
]
