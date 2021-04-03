from django.urls import path

from .import views

app_name = 'admins'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('pending-posts/', views.pending_posts, name='pending_posts'),
    path('approved-posts/', views.approved_posts, name='approved_posts'),
    path('approve-post/<str:slug>/', views.approve_pending_posts, name='approve_pending_posts'),
]