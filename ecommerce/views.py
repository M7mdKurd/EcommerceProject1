from django.contrib.auth import login, user_logged_in
from django.contrib.auth.models import AbstractUser, User
from django.core.serializers import serialize
from django.template.context_processors import request
from rest_framework import viewsets, status, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from ecommerce.models import Category, Products
from ecommerce.serializers import RegisterSerializer, LoginSerializer


#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#
#
# class RegisterView(APIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer




class AuthViewSet(ViewSet):

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise ValidationError('Incorrect username or password.')

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data['email']
        Token.objects.get_or_create(username=username, password=password , email=email)
        # Token.objects.get_or_create(username=username)

        return Response({'message': f'Hello {username}.'},status=status.HTTP_201_CREATED)





















