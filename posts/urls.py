from django.urls import path

from .import views

app_name = 'posts'

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
]