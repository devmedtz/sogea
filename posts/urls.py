from django.urls import path

from .import views

app_name = 'posts'

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('save-post-bookmark/', views.save_post_bookmark, name='save_post_bookmark'),
]