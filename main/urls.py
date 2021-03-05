from django.urls import path

from .import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:post_slug>/', views.post_detail, name='post_detail'),
]