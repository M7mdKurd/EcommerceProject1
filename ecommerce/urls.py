
from rest_framework.routers import DefaultRouter

from ecommerce.views import AuthViewSet, CategoryViewSet, ProductViewSet

router = DefaultRouter()

router.register('auth', AuthViewSet, basename='auth')
router.register('category', CategoryViewSet, basename='category_list')
router.register('product', ProductViewSet, basename='products')



urlpatterns = router.urls

