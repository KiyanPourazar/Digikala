from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from shop.models import Product
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from .cart import Cart
from shop.models import Product

@require_POST
def cart_remove(request):
    product_id = request.POST.get('product_id')
    cart = Cart(request)
    cart.remove(product_id)

    total_price = cart.get_total_price()
    return JsonResponse({'total_price': total_price})

@require_POST
def cart_update(request):
    product_id = request.POST.get('product_id')


def cart_summary(request):
    cart = Cart(request)
    cart_products = []
    total_price = 0

    for key, item in cart.cart.items():
        product = Product.objects.get(id=key)
        quantity = int(item.get('quantity', 1))
        total = product.price * quantity
        total_price += total

        cart_products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'total': total,
            'picture': product.picture,
        })

    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'total_price': total_price,
    })


@require_POST
def cart_add(request):
    if request.POST.get('action') == 'post':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        return JsonResponse({'message': 'success', 'cart_size': len(cart)})
    return JsonResponse({'message': 'error'})


def cart_remove(request):
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        cart.remove(product_id)

        total_price = cart.get_total_price()
        return JsonResponse({'total_price': total_price})
    return HttpResponseBadRequest("Invalid request")

def cart_update(request):
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, quantity=quantity)

        item_total = product.price * quantity
        total_price = cart.get_total_price()

        return JsonResponse({
            'item_total': item_total,
            'total_price': total_price,
        })
    return HttpResponseBadRequest("Invalid request")