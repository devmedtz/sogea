from django.urls import path

from .import views

app_name = 'marketing'

urlpatterns = [
    path('email-signup/', views.email_list_signup, name='email-list-signup'),
]