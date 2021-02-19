from django.shortcuts import render


def homepage(request):

    template_name = 'main/index.html'

    return render(request, template_name)
