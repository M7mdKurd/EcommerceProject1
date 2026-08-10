from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth import authenticate
from rest_framework import serializers

from ecommerce.models import Cart, CartItem, Order, OrderItem, Products, Category
from django.contrib.auth.models import User


# FOR FOREIGN KEYS THERE ARE TWO IDS

class RegisterSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'email': {'required': True , 'allow_blank' : False}}


class LoginSerializer (serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer

    class Meta:
        model = Products
        fields = ['id','name','price','description','stock','category_id']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source=AUTH_USER_MODEL)

    class Meta:
        model = Cart
        fields = ['id','user','created_at']
        #There is user_id_id also?


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer
    product = ProductSerializer

    class Meta:
        model = CartItem
        fields = ['id','cart_id','quantity','out_of_stock','product_id']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source=AUTH_USER_MODEL)

    class Meta:
        model = Order
        fields = ['id','user','created_at']



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    order = OrderSerializer

    class Meta:
        model = OrderItem
        fields = ['id','order_id','product_id']





