from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.auth.views import LogoutView

from apps.auth.views import ActivateUserView, RecoverRequestView, RecoveryPasswordView

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='auth_login'),
    path('refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('activate/<str:token>/', ActivateUserView.as_view(), name='auth_activate_account'),
    path('recovery', RecoverRequestView.as_view(), name='auth_recover_password'),
    path('recovery/<str:token>/', RecoveryPasswordView.as_view(), name='auth_reset_password'),
    path('logout', LogoutView.as_view(), name='auth_logout'),
]
