from django.urls import path

from .import views

app_name = 'posts'

urlpatterns = [
    path('write-post/', views.create_edit_post, name='create_post'),
    path('<int:id>/edit/', views.create_edit_post, name="edit_post"),
    path('<int:id>/delete/', views.delete_post, name='delete_post'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path('save-post-bookmark/', views.save_post_bookmark, name='save_post_bookmark'),
    path('follow/', views.follow_profile, name='follow_profile'),
    path('search/', views.search, name='search'),

    path('save_likes/', views.save_likes, name='save_likes'),

    path('ajax-authenticate-user/', views.ajax_authenticate_user, name='ajax_authenticate_user'),

    #Comment Crud
    path("comment/create/<int:post_pk>", views.CommentCreate.as_view(), name="create-comment"),

    path("comment/update/<int:pk>/", views.CommentUpdate.as_view(), name="update-comment"),

    path("comment/delete/<int:pk>/", views.CommentDelete.as_view(), name="delete-comment"),

    #Reply Crud
    path("reply/create/<int:comment_pk>", views.ReplyCreate.as_view(), name="create-reply"),

    path("reply/update/<int:pk>/", views.ReplyUpdate.as_view(), name="update-reply"),

    path("reply/delete/<int:pk>/", views.ReplyDelete.as_view(), name="delete-reply"),
]