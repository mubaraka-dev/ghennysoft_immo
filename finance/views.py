from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rent, Payment, SupplierInvoice,Contract
from .serializers import RentSerializer, PaymentSerializer, SupplierInvoiceSerializer,ContractSerializer
from django.db.models import Sum, Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes
from rest_framework.exceptions import MethodNotAllowed
@extend_schema_view(
    list=extend_schema(
        summary="Lister les loyers",
        description="Récupère la liste des loyers générés. Permet de filtrer par statut et contrat, et de rechercher par nom de locataire ou numéro d'appartement."
    ),
    retrieve=extend_schema(
        summary="Détails d'un loyer",
        description="Récupère les détails complets d'un loyer spécifique."
    ),
    create=extend_schema(
        summary="Créer un loyer",
        description="Crée manuellement un enregistrement de loyer."
    ),
    update=extend_schema(
        summary="Mettre à jour un loyer",
        description="Met à jour toutes les informations d'un loyer existant."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'un loyer",
        description="Met à jour partiellement les informations d'un loyer."
    ),
    destroy=extend_schema(
        summary="Supprimer un loyer",
        description="Supprime un enregistrement de loyer."
    ),
)
@extend_schema(tags=['Finance - Loyers'])
class RentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les loyers.
    Permet de lister, créer, voir les détails, mettre à jour et supprimer les loyers.
    Inclut une action pour générer les loyers mensuels en masse.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['contract__tenant__first_name', 'contract__apartment__number']
    filterset_fields = ['status', 'contract']

    @extend_schema(
        summary="Générer les loyers mensuels",
        description="Génère automatiquement les loyers pour tous les contrats actifs pour une année et un mois donnés.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'year': {'type': 'integer', 'description': 'Année (ex: 2023)'},
                    'month': {'type': 'integer', 'description': 'Mois (1-12)'},
                },
                'required': ['year', 'month']
            }
        },
        responses={
            201: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT
        }
    )
    @action(detail=False, methods=['post'])
    def generate_monthly_rents(self, request):
        """
        Logique pour générer les loyers pour tous les contrats actifs pour un mois donné.
        Attend 'year' et 'month' dans les données de la requête.
        """
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

@extend_schema_view(
    list=extend_schema(
        summary="Lister les paiements",
        description="Récupère l'historique des paiements effectués."
    ),
    retrieve=extend_schema(
        summary="Détails d'un paiement",
        description="Récupère les détails d'un paiement spécifique."
    ),
    create=extend_schema(
        summary="Enregistrer un paiement",
        description="Enregistre un nouveau paiement pour un loyer. Le statut du loyer est mis à jour automatiquement en fonction du montant payé."
    ),
    update=extend_schema(
        summary="Mettre à jour un paiement",
        description="Met à jour un paiement existant."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'un paiement",
        description="Met à jour partiellement un paiement."
    ),
    destroy=extend_schema(
        summary="Supprimer un paiement",
        description="Supprime un paiement."
    ),
)
@extend_schema(tags=['Finance - Paiements'])
class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les paiements de loyers.
    Lors de la création d'un paiement, le statut du loyer associé est mis à jour (PARTIAL ou PAID).
    """
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

@extend_schema_view(
    list=extend_schema(
        summary="Lister les factures fournisseurs",
        description="Récupère la liste des factures fournisseurs (électricité, eau, etc.)."
    ),
    retrieve=extend_schema(
        summary="Détails d'une facture",
        description="Récupère les détails d'une facture fournisseur spécifique."
    ),
    create=extend_schema(
        summary="Enregistrer une facture",
        description="Enregistre une nouvelle facture fournisseur."
    ),
    update=extend_schema(
        summary="Mettre à jour une facture",
        description="Met à jour une facture fournisseur."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'une facture",
        description="Met à jour partiellement une facture fournisseur."
    ),
    destroy=extend_schema(
        summary="Supprimer une facture",
        description="Supprime une facture fournisseur."
    ),
)
@extend_schema(tags=['Finance - Factures Fournisseurs'])
class SupplierInvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les factures des fournisseurs (SNEL, REGIDESO, etc.).
    """
    queryset = SupplierInvoice.objects.all()
    serializer_class = SupplierInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['provider', 'status', 'gallery']


@extend_schema_view(
    list=extend_schema(
        summary="Lister mes contrats",
        description="Récupère la liste des contrats où l'utilisateur connecté est soit le propriétaire, soit le locataire."
    ),
    retrieve=extend_schema(
        summary="Détails d'un contrat",
        description="Récupère les détails d'un contrat spécifique."
    ),
    create=extend_schema(
        summary="Créer un contrat",
        description="Crée un nouveau contrat. Le propriétaire est automatiquement défini sur l'utilisateur connecté."
    ),
    update=extend_schema(
        summary="Mettre à jour un contrat",
        description="Met à jour un contrat existant."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'un contrat",
        description="Met à jour partiellement un contrat."
    ),
    destroy=extend_schema(
        summary="Supprimer un contrat",
        description="Supprime un contrat."
    ),
)
@extend_schema(tags=['Finance - Contrats propriétaire/locataire'])
class ContractViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les contrats.
    - Le propriétaire (créateur) a tous les droits.
    - Le locataire a un accès en lecture seule.
    """
    queryset = Contract.objects.all()  # Nécessaire pour le router, même si get_queryset est défini
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tenant__first_name', 'tenant__last_name', 'apartment__number']
    filterset_fields = ['is_active', 'apartment']

    def get_permissions(self):
        """Définit les permissions spécifiques : seul le propriétaire peut modifier/supprimer."""
        if self.action in ['update', 'partial_update', 'destroy']:
            # On vérifie que l'utilisateur est bien le propriétaire dans has_object_permission plus bas ou via une classe dédiée
            # Ici, on utilise une logique simple : on surcharge check_object_permissions ou on utilise une classe custom.
            # Pour faire simple et robuste dans ce fichier, on ajoute une classe de permission dynamique ici :
            class IsOwnerOrReadOnly(permissions.BasePermission):
                def has_object_permission(self, request, view, obj):
                    # Lecture autorisée pour tout le monde (filtré par get_queryset)
                    if request.method in permissions.SAFE_METHODS:
                        return True
                    # Écriture/Suppression uniquement pour le propriétaire
                    return obj.owner == request.user
            return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Cette vue retourne une liste de tous les contrats pour l'utilisateur
        actuellement authentifié, où il est soit le propriétaire (owner),
        soit le locataire (tenant).
        """
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Contract.objects.none()
        return Contract.objects.filter(Q(owner=user) | Q(tenant=user))

    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme propriétaire du contrat."""
        serializer.save(owner=self.request.user)

    # empecher les méthodes de suppression et de mise à jour des contrats
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')





# finance/views.py
# finance/views.py
from django.http import HttpResponse
from .models import Rent

def run_rents_cron(request):
    Rent.process_rents()
    return HttpResponse(status=204)



