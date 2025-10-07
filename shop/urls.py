from django.urls import path
from .views import ProductsView, about, login_user, logout_user, register_user

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('about/', about, name='about'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',register_user,name='register'),
]
