from django.urls import path
from django.contrib.auth import views as auth_views

from .import views

app_name = 'accounts'
 
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),

    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view() ,name='password_change_done'),
]