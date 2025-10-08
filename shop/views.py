from .models import Product
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login

def products_view(request):
    all_products = Product.objects.all()
    return render(request, 'index.html', {"all_products": all_products})

def about(request):
    return render(request, 'about.html')

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
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not email or not password1 or not password2:
            messages.error(request, "لطفاً تمام فیلدها را پر کنید.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "رمز عبور و تکرار آن مطابقت ندارند.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "این ایمیل قبلاً ثبت شده است.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        login(request, user)
        messages.success(request, "ثبت‌نام با موفقیت انجام شد! خوش آمدید 🎉")
        return redirect("products")

    return render(request, "register.html")