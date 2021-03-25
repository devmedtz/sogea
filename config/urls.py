from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('accounts/', include('allauth.urls')),

    path('posts/', include('posts.urls', namespace='posts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('s3direct/', include('s3direct.urls')),

    path('comment/', include('comment.urls')),
    path('api/', include('comment.api.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
