import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from books.models import Book, Category

def home(request):
    books = Book.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('id')[:24]
    context = {
        'categories':categories,
        'books':books
    }
    template_name = 'books/index.html'
    return render(request, template_name, context)


@login_required
def book_details(request, slug):

    book = get_object_or_404(Book, slug=slug)

    context = {
        'book':book
    }
    template_name = 'books/book_detail.html'
    return render(request, template_name, context)


@login_required
def download_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    filename =  os.path.basename(book.file.name)
    file = book.file
    if file:
        response = HttpResponse(file, content_type='application/pdf')
        download = request.POST.get("download")
        content = "filename=%s" %(filename)
        if download:
            book.downloads += 1
            book.save()
            content = content
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")