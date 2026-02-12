from rest_framework import viewsets, permissions, filters
from .models import Gallery, Apartment
from .serializers import GallerySerializer, ApartmentSerializer, UserGallerySerializer, UserApartmentSerializer
from .permissions import IsOwner
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
 
@extend_schema_view(
    list=extend_schema(
        summary="Lister les galeries",
        description="Récupère une liste de toutes les galeries. Permet la recherche par nom, adresse et nom du manager."
    ),
    retrieve=extend_schema(
        summary="Détails d'une galerie",
        description="Récupère les détails complets d'une galerie spécifique, y compris la liste des appartements associés."
    ),
    create=extend_schema(
        summary="Créer une nouvelle galerie",
        description="Crée un nouvel enregistrement de galerie."
    ),
    update=extend_schema(
        summary="Mettre à jour une galerie",
        description="Met à jour complètement les informations d'une galerie existante."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'une galerie",
        description="Met à jour partiellement les informations d'une galerie existante."
    ),
    destroy=extend_schema(
        summary="Supprimer une galerie",
        description="Supprime une galerie de la base de données."
    ),
)
@extend_schema(tags=['Propriétés - Galeries'])
class GalleryViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les galeries.
    Fournit des points de terminaison pour lister, créer, récupérer, mettre à jour et supprimer des galeries.
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address', 'manager_name']

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
    create=extend_schema(
        summary="Créer un nouvel appartement",
        description="Crée un nouvel enregistrement d'appartement pour une galerie donnée."
    ),
    update=extend_schema(
        summary="Mettre à jour un appartement",
        description="Met à jour complètement les informations d'un appartement existant."
    ),
    partial_update=extend_schema(
        summary="Mise à jour partielle d'un appartement",
        description="Met à jour partiellement les informations d'un appartement existant."
    ),
    destroy=extend_schema(
        summary="Supprimer un appartement",
        description="Supprime un appartement de la base de données."
    ),
)
@extend_schema(tags=['Propriétés - Appartements'])
class ApartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les appartements.
    Fournit des points de terminaison pour lister, créer, récupérer, mettre à jour et supprimer des appartements.
    """
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
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
    search_fields = ['name', 'address', 'manager_name']

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
