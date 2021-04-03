from django.urls import path

from .import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('yesterday/posts/', views.yesterday_posts, name='yesterday_posts'),
    path('weekly/posts/', views.weekly_posts, name='week-post'),
    path('monthly/posts/', views.monthly_posts, name='month-post'),
    path('yearly/posts/', views.yearly_posts, name='year-post'),
    path('<slug:post_slug>/', views.post_detail, name='post_detail'),

    path('pages/code-of-conducts/', views.code_of_conduct, name='code_of_conduct'),
    path('pages/terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('pages/privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('pages/contacts/', views.contacts, name='contacts'),
    path('pages/about/', views.about, name='about'),
    path('pages/faq/', views.FAQ, name='faq'),
   
]