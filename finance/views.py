from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rent, Payment, SupplierInvoice
from .serializers import RentSerializer, PaymentSerializer, SupplierInvoiceSerializer
from django.db.models import Sum

class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['contract__tenant__first_name', 'contract__apartment__number']
    filterset_fields = ['status', 'contract']

    @action(detail=False, methods=['post'])
    def generate_monthly_rents(self, request):
        # Logic to generate rents for all active contracts for a given month
        # This is a simplified version
        # Expects 'year' and 'month' in data
        from tenants.models import Contract
        from datetime import date
        
        year = request.data.get('year')
        month = request.data.get('month')
        
        if not year or not month:
            return Response({'error': 'Year and Month required'}, status=status.HTTP_400_BAD_REQUEST)
            
        active_contracts = Contract.objects.filter(is_active=True)
        created_count = 0
        
        for contract in active_contracts:
            # Check if rent already exists
            start_date = date(int(year), int(month), 1)
            # Simple logic for end date (end of month)
            import calendar
            last_day = calendar.monthrange(int(year), int(month))[1]
            end_date = date(int(year), int(month), last_day)
            
            if not Rent.objects.filter(contract=contract, period_start=start_date).exists():
                Rent.objects.create(
                    contract=contract,
                    period_start=start_date,
                    period_end=end_date,
                    due_date=date(int(year), int(month), 5), # Example due date: 5th of month
                    amount=contract.rent_amount
                )
                created_count += 1
                
        return Response({'message': f'{created_count} rents generated'}, status=status.HTTP_201_CREATED)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['rent', 'method']

    def perform_create(self, serializer):
        payment = serializer.save()
        # Update rent status
        rent = payment.rent
        if rent.balance <= 0:
            rent.status = 'PAID'
        elif rent.total_paid > 0:
            rent.status = 'PARTIAL'
        rent.save()

class SupplierInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SupplierInvoice.objects.all()
    serializer_class = SupplierInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['provider', 'status', 'gallery']
