from django.urls import path, include
from rest_framework import views
from rest_framework.routers import DefaultRouter
from ecommerce import views
from .views import AuthViewset
from ecommerce.serializers import RegisterSerializer

# from ecommerce.views import CategoryViewSet, ProductViewSet, RegisterView

router = DefaultRouter()

# router.register('categories',CategoryViewSet, basename='category')
# router.register('products',ProductViewSet, basename='product')

router.register('auth', AuthViewset, basename='auth')


urlpatterns = router.urls

