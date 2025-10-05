from django.views import View
from django.shortcuts import render
from .models import Product

class ProductsView(View):
    def get(self, request):
        all_products = Product.objects.all()
        return render(request, 'index.html', {"all_products": all_products})