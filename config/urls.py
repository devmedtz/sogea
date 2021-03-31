from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('accounts/', include('allauth.urls')),
    path('account/', include('accounts.urls', namespace='account')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    path('admin/', include('admins.urls', namespace='admins')),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('comment/', include('comment.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
