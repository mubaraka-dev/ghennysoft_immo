from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'contracts', ContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
