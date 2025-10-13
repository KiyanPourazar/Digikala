from django.urls import path
from .views import shop_view, about, login_user, logout_user, register_user, product_view, category_view

urlpatterns = [
    path('', shop_view, name='shop'),
    path('about/', about, name='about'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',register_user,name='register'),
    path('product/<int:pk>',product_view,name='product'),
    path('category/<str:cat>', category_view, name='category'),

]
