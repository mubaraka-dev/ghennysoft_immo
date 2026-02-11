from rest_framework import permissions
from .models import UserChoice


class IsAdminOrSelf(permissions.BasePermission):
    """
    - Création libre (inscription)
    - Admins (SUPER_ADMIN, MANAGER) : accès total
    - Utilisateur normal : accès uniquement à son propre profil
    """

    def has_permission(self, request, view):
        # Autoriser l'inscription sans authentification
        if view.action == 'create':
            return True

        # Toutes les autres actions nécessitent authentification
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins → accès total
        # if request.user.role in [UserChoice.SUPER_ADMIN, UserChoice.MANAGER]:
        #     return True

        # Sinon → seulement son propre compte
        return obj == request.user
