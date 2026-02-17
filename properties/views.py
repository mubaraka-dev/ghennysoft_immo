from rest_framework import viewsets, permissions, filters
from .models import Gallery, Apartment, GalleryManager
from .serializers import GallerySerializer, ApartmentSerializer, UserGallerySerializer, UserApartmentSerializer, GalleryManagerSerializer
from .permissions import IsOwner
from .permissions_properties import ownerPropertiesPermission
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
 
@extend_schema_view(
    list=extend_schema(
        summary="Lister les galeries",
        description="Récupère une liste de toutes les galeries. Permet la recherche par nom."
    ),
    retrieve=extend_schema(
        summary="Détails d'une galerie",
        description="Récupère les détails complets d'une galerie spécifique, y compris la liste des appartements associés."
    ),
)
@extend_schema(tags=['Propriétés - Galeries'])
class GalleryList(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la consultation des galeries.
    Fournit des points de terminaison pour lister et voir les détails des galeries.
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    def get_queryset(self):
        """
        Optimise le queryset en préchargeant les appartements associés
        et en annotant le nombre total d'appartements pour éviter les requêtes N+1.
        """
        return super().get_queryset().prefetch_related('apartments').annotate(
            total_apartments=Count('apartments')
        )

@extend_schema_view(
    list=extend_schema(
        summary="Lister les appartements",
        description="Récupère une liste de tous les appartements. Permet de filtrer par galerie et statut, et de rechercher par numéro d'appartement ou nom de la galerie."
    ),
    retrieve=extend_schema(
        summary="Détails d'un appartement",
        description="Récupère les détails complets d'un appartement spécifique."
    ),
)
@extend_schema(tags=['Propriétés - Appartements'])
class ApartmentList(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour la consultation des appartements.
    Fournit des points de terminaison pour lister et voir les détails des appartements.
    L'accès est public pour la liste et le détail.
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number', 'gallery__name']
    filterset_fields = ['gallery', 'status']

    def get_queryset(self):
        """
        Optimise le queryset en utilisant select_related pour récupérer
        la galerie associée dans la même requête de base de données.
        """
        return super().get_queryset().select_related('gallery')


#  les donnes de l'utilisateur qui est connecté en session: ses données de galerie et d'appartement
# proprietaire de ces galery

@extend_schema_view(
    list=extend_schema(
        summary="Lister mes galeries",
        description="Récupère la liste des galeries appartenant à l'utilisateur connecté."
    ),
    retrieve=extend_schema(
        summary="Détails d'une galerie",
        description="Récupère les détails d'une galerie spécifique appartenant à l'utilisateur."
    ),
    create=extend_schema(
        summary="Créer une galerie",
        description="Crée une nouvelle galerie pour l'utilisateur connecté."
    ),
    update=extend_schema(
        summary="Mettre à jour une galerie",
        description="Met à jour une galerie existante."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle",
        description="Met à jour partiellement une galerie."
    ),
    destroy=extend_schema(
        summary="Supprimer une galerie",
        description="Supprime une galerie."
    ),
)
@extend_schema(tags=['Propriétés - Mes Galeries'])
class UserGalleryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les galeries de l'utilisateur connecté.
    """
    serializer_class = UserGallerySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']

    def get_queryset(self):
        # Pour la génération de schéma Swagger (évite l'erreur sur request.user)
        if getattr(self, 'swagger_fake_view', False):
            return Gallery.objects.none()
        return Gallery.objects.filter(owner=self.request.user).prefetch_related('apartments').annotate(
            total_apartments=Count('apartments')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema_view(
    list=extend_schema(
        summary="Lister mes appartements",
        description="Récupère la liste des appartements appartenant à l'utilisateur connecté (via ses galeries)."
    ),
    retrieve=extend_schema(
        summary="Détails d'un appartement",
        description="Récupère les détails d'un appartement spécifique appartenant à l'utilisateur."
    ),
    create=extend_schema(
        summary="Créer un appartement",
        description="Crée un nouvel appartement dans une galerie appartenant à l'utilisateur."
    ),
    update=extend_schema(
        summary="Mettre à jour un appartement",
        description="Met à jour un appartement existant."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle",
        description="Met à jour partiellement un appartement."
    ),
    destroy=extend_schema(
        summary="Supprimer un appartement",
        description="Supprime un appartement."
    ),
)
@extend_schema(tags=['Propriétés - Mes Appartements'])
class UserApartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les appartements de l'utilisateur connecté.
    """
    serializer_class = UserApartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['number', 'gallery__name']
    filterset_fields = ['gallery', 'status']

    def get_queryset(self):
        # Pour la génération de schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Apartment.objects.none()
        return Apartment.objects.filter(gallery__owner=self.request.user).select_related('gallery')

    def perform_create(self, serializer):
        # Vérification de sécurité : la galerie choisie doit appartenir à l'utilisateur
        gallery = serializer.validated_data.get('gallery')
        if gallery and gallery.owner != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous ne pouvez pas ajouter d'appartement dans une galerie qui ne vous appartient pas.")
        serializer.save()

@extend_schema_view(
    list=extend_schema(
        summary="Lister les managers de vos gallery",
        description="Récupère la liste des assignations de managers pour vos gallery."
    ),
    retrieve=extend_schema(
        summary="Détails d'une assignation",
        description="Récupère les détails d'une assignation manager-appartement."
    ),
    create=extend_schema(
        summary="Assigner un manager",
        description="Assigne un manager à un appartement spécifique."
    ),
    update=extend_schema(
        summary="Mettre à jour une assignation",
        description="Met à jour l'assignation d'un manager."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle",
        description="Met à jour partiellement une assignation."
    ),
    destroy=extend_schema(
        summary="Supprimer une assignation",
        description="Supprime l'assignation d'un manager à un appartement."
    ),
)
@extend_schema(tags=['Propriétés - Gestionnaires'])
class GalleryManagerViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les managers assignés aux galeries.
    Accessible uniquement par le propriétaire des galeries.
    """
    serializer_class = GalleryManagerSerializer
    permission_classes = [ownerPropertiesPermission]

    def get_queryset(self):
        # Pour la génération de schéma Swagger
        if getattr(self, 'swagger_fake_view', False):
            return GalleryManager.objects.none()
        return GalleryManager.objects.filter(gallery__owner=self.request.user)
