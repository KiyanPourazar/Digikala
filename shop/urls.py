from django.urls import path
from .views import ProductsView, about

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('about/', about, name='about'),
]
