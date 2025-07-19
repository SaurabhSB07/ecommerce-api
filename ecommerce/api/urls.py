from django.urls import path
from .views import (
    UserRegisterationView, UserLoginView, UserPasswordResetView,
    UserChagePasswordResetEmailRequestView, UserChangePasswordView, UserProfileView
)

urlpatterns = [
    path('register/', UserRegisterationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name="changepassword"),
    path('reset-password-email-request/', UserChagePasswordResetEmailRequestView.as_view(), name="reset-password-email-request"),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name="reset-password"),
]
