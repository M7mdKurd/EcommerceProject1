
from django.db import models
from django.contrib.auth.models import User


from rest_framework.authtoken.models import Token



class Category(models.Model):
    name = models.CharField(max_length=40)


class Products(models.Model):
    name = models.CharField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE, null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class Order(models.Model):
    user_id = models.OneToOneField(User ,on_delete=models.CASCADE, null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)



