from rest_framework import permissions

class ownerPropertiesPermission(permissions.BasePermission):
    """
    Permission personnalisée pour permettre uniquement au propriétaire de la galerie
    (et donc de l'appartement) de gérer les managers d'appartement.
    """
    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj est une instance de ApartmentManager
        # On vérifie si le propriétaire de la galerie est l'utilisateur connecté
        return obj.gallery.owner == request.user
