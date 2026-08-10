from django.urls import path, include
from rest_framework import views
from rest_framework.routers import DefaultRouter
from ecommerce import views
from .views import AuthViewSet
from ecommerce.serializers import RegisterSerializer

# from ecommerce.views import CategoryViewSet, ProductViewSet, RegisterView

router = DefaultRouter()

router.register('auth', AuthViewSet, basename='auth')


urlpatterns = router.urls

