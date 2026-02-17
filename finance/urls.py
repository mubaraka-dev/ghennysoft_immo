from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentViewSet, PaymentViewSet, SupplierInvoiceViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'rents', RentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'invoices', SupplierInvoiceViewSet)
router.register(r'contracts', ContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
