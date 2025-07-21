from django.urls import path,include
from .views import (
    UserRegisterationView, UserLoginView, UserPasswordResetView,
    UserChagePasswordResetEmailRequestView, UserChangePasswordView, UserProfileView
)
from .views import ProductView,CartView,CartItemView,OrderViewSet,OrderItemViewSet
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(f'products',ProductView,basename='product')
router.register(r'carts', CartView, basename='cart')
router.register(r'cart-items', CartItemView, basename='cartitem')
router.register(f'orders',OrderItemViewSet,basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')


urlpatterns = [
    path('register/', UserRegisterationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name="changepassword"),
    path('reset-password-email-request/', UserChagePasswordResetEmailRequestView.as_view(), name="reset-password-email-request"),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name="reset-password"),
]

urlpatterns += router.urls