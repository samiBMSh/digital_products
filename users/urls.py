from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterView, GetTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register panel'),
    # path('get-token/', GetTokenView.as_view(), name='token panel'),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
