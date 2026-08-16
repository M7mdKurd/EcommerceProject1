from logging import raiseExceptions

from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ecommerce.models import Category, Products, Cart, CartItem, Order, OrderItem
from ecommerce.serializers import RegisterSerializer, LoginSerializer, CategorySerializer, ProductSerializer, \
    CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer



class AuthViewSet(ViewSet):

    @action(detail=False, methods=['post'] , permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            username = User.objects.get(username=username)
            if username.check_password(password):
                token, created = Token.objects.get_or_create(user=username)
                return Response({'token': token.key, 'username': username.username})
            return Response({'message': 'Username / Password is Invalid'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



    @action(detail=False, methods=['post'] , permission_classes=[AllowAny])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        User.objects.create_user(username=username, password=password , email=email)

        return Response({'message': f'Hello {username}.'},status=status.HTTP_201_CREATED)





class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer





class CartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_items(self, request, *args, **kwargs):
        serializer = CartItemSerializer(many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializers = CartSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        cart, created = Cart.objects.get_or_create(user_id=serializers.validated_data['user_id'])


        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=serializer.validated_data['product_id'],
            quantity=serializer.validated_data['quantity'],
        )

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['delete'], url_path='delete-item')
    def delete_item(self, request, pk=None):
        Cart.objects.filter(id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['put'], url_path='add-item')
    def update_quantity(self, request, pk=None):
        serializers = CartItemSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        cart_item = CartItem.objects.get(id=pk)
        cart_item.quantity = request.data.get('quantity',cart_item.quantity)
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    @action(detail=False, methods=['delete'], url_path='clear-cart')
    def clear_cart(self, request):
        Cart.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

