from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page


def index(request):
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # # return HttpResponse('Rango!')
    # return render(request, 'rango/index.html', context=context_dict)
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {"first": "shen", "second": "wei"}
    return render(request, 'rango/about.html', context=context_dict)
