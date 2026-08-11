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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer

    class Meta:
        model = Products
        fields = ['id','name','price','description','stock','category']


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Cart
        fields = ['id','user_id','created_at']
        #There is user_id_id also?


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer
    product = ProductSerializer
    class Meta:
        model = CartItem
        fields = ['id','cart','quantity','out_of_stock','product']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer

    class Meta:
        model = OrderItem
        fields = ['id','order_id','product']



class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','user_id','created_at','items']








