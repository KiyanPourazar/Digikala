class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'price': product.price,
                'quantity': 1,
                'picture': product.picture.url if product.picture else '',
            }
        else:
            self.cart[product_id]['quantity'] += 1

        self.save()

    def remove(self, product_id):
        """حذف محصول از سبد"""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product_id, quantity):
        """به‌روزرسانی تعداد محصول"""
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        """جمع کل سبد خرید"""
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def __len__(self):
        """تعداد کل آیتم‌ها"""
        return sum(item['quantity'] for item in self.cart.values())
