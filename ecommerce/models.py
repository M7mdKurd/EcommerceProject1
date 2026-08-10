from django.conf import settings
from django.contrib.auth import login
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token



class Category(models.Model):
    name = models.CharField(max_length=40,null= True)


class Products(models.Model):
    name = models.CharField
    price = models.DecimalField
    description = models.TextField
    stock = models.IntegerField(default=0)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Cart(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    out_of_stock = models.BooleanField(default=False)
    product_id = models.OneToOneField(Products, on_delete=models.CASCADE)


class Order(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.OneToOneField(Products, on_delete=models.CASCADE)



