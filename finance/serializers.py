from rest_framework import serializers
from .models import Rent, Payment, SupplierInvoice

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class RentSerializer(serializers.ModelSerializer):
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tenant_name = serializers.ReadOnlyField(source='contract.tenant.first_name')
    apartment_details = serializers.ReadOnlyField(source='contract.apartment.number')

    class Meta:
        model = Rent
        fields = '__all__'

class SupplierInvoiceSerializer(serializers.ModelSerializer):
    gallery_name = serializers.ReadOnlyField(source='gallery.name')
    apartment_number = serializers.ReadOnlyField(source='apartment.number')

    class Meta:
        model = SupplierInvoice
        fields = '__all__'
