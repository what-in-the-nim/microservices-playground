from django.shortcuts import render

from .models import Product


def menu(request):
    products = Product.objects.all()
    return render(request, "menu/menu.html", {"products": products})
