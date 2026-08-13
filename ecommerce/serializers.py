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


class CartItemSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='item_total', max_digits=10, decimal_places=2, read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)



    class Meta:
        model = CartItem
        fields = ['id','cart_id','quantity','product_id','product_name','price','product_description']

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



class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()


    class Meta:
        model = Cart
        fields = ['id','user_id','created_at','total_amount','cart_items']

    def validate(self, attrs):
        try:
            User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User")
        return attrs

    def get_total_amount(self,obj):
        cart_items = obj.cart_items.all()
        return sum(cart_items.item_total for cart_items in cart_items)





class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='item_total', max_digits=10, decimal_places=2, read_only=True)
    product_description = serializers.CharField(source='product.description', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','order_id','quantity','product_id','product_name','price','product_description']


    def validate(self, attrs):
        if attrs['quantity'] > Products.objects.get(id=attrs['product_id']).stock:
            raise serializers.ValidationError("Out of Stock")
        try:
            Order.objects.get(id=attrs['order_id'])
        except Order.DoesNotExist:
            raise serializers.ValidationError("Invalid Order")


        return attrs



class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','user_id','created_at','order_items']

    def validate(self, attrs):
        try:
            User.objects.get(id=attrs['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid User")
        return attrs

    def get_total_amount(self,obj):
        order_items = obj.order_items.all()
        return sum(order_items.item_total for order_items in order_items)
