
from rest_framework.routers import DefaultRouter

from ecommerce.views import AuthViewSet, CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, \
    OrderItemViewSet

router = DefaultRouter()

router.register('auth', AuthViewSet, basename='auth')
router.register('category', CategoryViewSet, basename='category_list')
router.register('product', ProductViewSet, basename='products')
router.register('cart', CartViewSet, basename='cart')
router.register('order', OrderViewSet, basename='order')
router.register('order-item', OrderItemViewSet, basename='order item')


urlpatterns = router.urls

