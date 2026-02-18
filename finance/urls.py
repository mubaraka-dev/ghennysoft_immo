from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentViewSet, PaymentViewSet, SupplierInvoiceViewSet, ContractViewSet, run_rents_cron

router = DefaultRouter()
router.register(r'rents', RentViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'invoices', SupplierInvoiceViewSet)
router.register(r'contracts', ContractViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('run-rents-cron/', run_rents_cron, name='run_rents_cron'),
]
