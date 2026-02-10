from rest_framework import serializers
from .models import Tenant, Contract

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.first_name')
    apartment_details = serializers.ReadOnlyField(source='apartment.number')
    
    class Meta:
        model = Contract
        fields = '__all__'
