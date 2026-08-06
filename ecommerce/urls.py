from django.urls import path, include
from rest_framework import views
from rest_framework.routers import DefaultRouter
from ecommerce import views

from ecommerce.serializers import RegisterSerializer

# from ecommerce.views import CategoryViewSet, ProductViewSet, RegisterView
#
# router = DefaultRouter()
#
# # router.register('categories',CategoryViewSet, basename='category')
# # router.register('products',ProductViewSet, basename='product')
#
# router.register('signup', RegisterSerializer, basename='signup')
#
#
# urlpatterns = router.urls

urlpatterns = [
    path('auth/signup/', views.AuthSignUp.as_view(), name='register'),

]
