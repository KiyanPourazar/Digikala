from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name_plural = 'Customers'

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='upload/product/')

    is_sale = models.BooleanField(default=False)
    sale_price = models.FloatField()

    STAR_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    star = models.IntegerField(default=0, choices=STAR_CHOICES)

    SIZE_CHOICES = (
        ('None','None'),
        ('M', 32),
        ('L', 42),
        ('XL', 64),
    )
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, default='None')
    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
