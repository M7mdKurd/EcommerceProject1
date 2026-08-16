
from django.db import models
from django.contrib.auth.models import User


from rest_framework.authtoken.models import Token



class Category(models.Model):
    name = models.CharField(max_length=50)


class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    @property
    def count_order(self):
        return self.orderitem_set.count()


class Cart(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE, null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    @property
    def item_total(self):
        return self.quantity * self.product.price



class Order(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE, null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status_choices = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
    )
    order_status = models.CharField(max_length=10, choices=order_status_choices, default='pending')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.PROTECT)

    @property
    def item_total(self):
        return self.quantity * self.product.price

