from django.contrib.auth.models import AbstractUser, User
from rest_framework import viewsets, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ecommerce.models import Category, Products, Cart, CartItem
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



    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        User.objects.create_user(username=username, password=password , email=email)

        return Response({'message': f'Hello {username}.'},status=status.HTTP_201_CREATED)





class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, pk=None):
        Category.objects.get(pk=pk).delete()
        return Response({'message': 'Deleted'}  ,status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer



class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def delete(self, request, pk=None):
        Cart.objects.get(pk=pk).delete()
        return Response({'message': 'Deleted'}  ,status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def delete(self, request, pk=None):
        CartItem.objects.get(pk=pk).delete()
        return Response({'message': 'Deleted'}  ,status=status.HTTP_204_NO_CONTENT)



class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    serializer_class = OrderSerializer

    def delete(self, request, pk=None):
        Cart.objects.get(pk=pk).delete()
        return Response({'message': 'Deleted'}  ,status=status.HTTP_204_NO_CONTENT)


class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CartItem.objects.all()
    serializer_class = OrderItemSerializer

    def delete(self, request, pk=None):
        CartItem.objects.get(pk=pk).delete()
        return Response({'message': 'Deleted'}  ,status=status.HTTP_204_NO_CONTENT)