from django.urls import path

from .import views

app_name = 'admins'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]