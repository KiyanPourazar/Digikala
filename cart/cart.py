from decimal import Decimal

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        # قیمت نهایی: اگر فروش ویژه بود از sale_price استفاده کن
        final_price = float(product.sale_price) if getattr(product, 'is_sale', False) else float(product.price)

        if product_id in self.cart:
            # اگر اضافه می‌کنیم، موجودی انبار را رعایت کن
            new_quantity = self.cart[product_id]['quantity'] + quantity
            if new_quantity > getattr(product, 'stock', 9999):  # اگر stock نداریم، بی‌نهایت
                new_quantity = getattr(product, 'stock', 9999)
            self.cart[product_id]['quantity'] = new_quantity
        else:
            self.cart[product_id] = {
                'name': product.name,
                'price': final_price,
                'original_price': float(product.price),
                'sale_price': float(product.sale_price) if getattr(product, 'is_sale', False) else None,
                'is_sale': getattr(product, 'is_sale', False),
                'quantity': quantity,
                'picture': product.picture.url if product.picture else '',
                'stock': getattr(product, 'stock', 9999),
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            # بررسی موجودی
            stock = self.cart[product_id].get('stock', 9999)
            self.cart[product_id]['quantity'] = min(quantity, stock)
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
