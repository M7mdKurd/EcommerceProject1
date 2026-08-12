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
    category_id = serializers.IntegerField()
    stock = serializers.IntegerField(default=0)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255)

    class Meta:
        model = Products
        fields = ['id','name','price','description','stock','category_id']

    def validate(self, attrs):
        if attrs['stock'] < 1:
            raise serializers.ValidationError("Stock cannot be less than 1")
        try:
            Category.objects.get(id=attrs['category_id'])
        except Category.DoesNotExist:
            raise serializers.ValidationError("Invalid Category")
        if attrs['price'] < 0:
            raise serializers.ValidationError("Price cannot be less than 0")

        return attrs




class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['id','user_id','created_at']

    def validate(self, attrs):
        try:
            User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User")
        return attrs




class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


    class Meta:
        model = CartItem
        fields = ['id','cart_id','quantity','product_id']

    def validate(self, attrs):
        if attrs['quantity'] > Products.objects.get(id=attrs['product_id']).stock:
            raise serializers.ValidationError("Out of Stock")

        #PROBLEM HERE
        try:
            Products.objects.get(id=attrs['product_id'])
        except Products.DoesNotExist:
            raise serializers.ValidationError("Invalid Product")

        try:
            Cart.objects.get(id=attrs['cart_id'])
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Invalid Cart")

        return attrs




class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['id','user_id','created_at']

    def validate(self, attrs):
        try:
            User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User")
        return attrs



class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['id','order_id','quantity','product_id']


    def validate(self, attrs):
        try:
            Order.objects.get(id=attrs['order_id'])
        except Order.DoesNotExist:
            raise serializers.ValidationError("Invalid Order")

        if attrs['quantity'] > Products.objects.get(id=attrs['product_id']).stock:
            raise serializers.ValidationError("Out of Stock")

        return attrs

