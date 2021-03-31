from django.urls import path
from django.contrib.auth import views as auth_views

from .import views

app_name = 'accounts'
 
urlpatterns = [
    path('admin-login/', views.UserLoginView.as_view(), name='admin_login'),

    path('admin_logout/', auth_views.LogoutView.as_view(), name='admin_logout'),

    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view() ,name='password_change_done'),

    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
]