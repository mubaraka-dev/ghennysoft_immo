from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, ReadUpdateDeleteUserView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('read-update-delete/', ReadUpdateDeleteUserView.as_view(), name='read_update_delete_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
