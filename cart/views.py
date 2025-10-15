from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from shop.models import Product

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

        # بررسی موجودی
        current_quantity = cart.cart.get(str(product.id), {}).get('quantity', 0)
        if current_quantity + 1 > product.stock:
            return JsonResponse({'message': 'exceeds_stock', 'stock': product.stock}, status=400)

        cart.add(product=product)

        total_items = len(cart)

        return JsonResponse({
            'message': 'success',
            'total_items': total_items
        })
    return JsonResponse({'message': 'error'})


# views.py
@require_POST
def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    product = get_object_or_404(Product, id=product_id)

    # بررسی موجودی
    if quantity > product.stock:
        return JsonResponse({
            'error': f'تعداد انتخابی شما بیشتر از موجودی انبار است. حداکثر: {product.stock} عدد'
        }, status=400)

    # اگر همه چیز درست بود، سبد خرید را آپدیت کن
    cart.update(product_id=product_id, quantity=quantity)

    # چون قیمت تخفیف خورده در سشن ذخیره شده، از آنجا می‌خوانیم
    item_price = cart.cart[str(product.id)]['price']
    item_total = float(item_price) * quantity
    total_price = cart.get_total_price()
    total_items = len(cart)

    return JsonResponse({
        'message': 'updated',
        'item_total': item_total,
        'total_price': total_price,
        'total_items': total_items,
    })

@require_POST
def cart_remove(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    cart.remove(product_id)

    total_price = cart.get_total_price()
    total_items = len(cart)

    return JsonResponse({
        'message': 'removed',
        'total_price': total_price,
        'total_items': total_items
    })