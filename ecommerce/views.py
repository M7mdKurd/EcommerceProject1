from django.contrib.auth import login, user_logged_in
from django.contrib.auth.models import AbstractUser, User
from django.template.context_processors import request
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
# #
# class RegisterView(APIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer



# @api_view(['GET', 'POST'])
# def register(request):
#     if request.method == 'GET':
#         user = User.objects.all()
#         serializer = RegisterSerializer(user, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     return None



class AuthSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class AuthLogin(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]




# class AuthTest(generics.ListAPIView):

#     permission_classes = [IsAuthenticated]




















