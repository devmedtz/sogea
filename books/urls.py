from django.urls import path

from books.views import (
    books
)

app_name = 'books'

urlpatterns = [
    path('home/', books.home, name='home'),
    path('details/<str:slug>/', books.book_details, name='book_detail'),
    path('download/<str:slug>/', books.download_book, name='download_book'),
]