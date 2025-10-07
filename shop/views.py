from urllib import request

from django.views import View
from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages

class ProductsView(View):
    def get(self, request):
        all_products = Product.objects.all()
        return render(request, 'index.html', {"all_products": all_products})

def about(request):
    return render(request, 'about.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('login_field')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید!')
            return redirect('products')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید!')
    return redirect('products')

def register_user(request):
    return render(request, 'register.html')