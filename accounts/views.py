from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import UserChoice
from rest_framework import generics, viewsets ,status,permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

User = get_user_model()








@extend_schema(
    tags=['Utilisateurs'],
    summary="Créer un nouveau utilisateur",
    description="Créer un nouveau utilisateur.",
)
@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permet à tout le monde de créer un utilisateur


@extend_schema_view(
    get=extend_schema(
        summary="Récupérer mon profil",
        description="Récupère les informations de l'utilisateur actuellement connecté."
    ),
    put=extend_schema(
        summary="Mettre à jour mon profil",
        description="Met à jour les informations de l'utilisateur connecté."
    ),
    patch=extend_schema(
        summary="Mise à jour partielle de mon profil",
        description="Met à jour partiellement les informations de l'utilisateur connecté."
    ),
    delete=extend_schema(
        summary="Supprimer mon compte",
        description="Désactive le compte de l'utilisateur connecté (suppression logique)."
    ),
)
@extend_schema(tags=['Utilisateurs'])
class ReadUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    look_up_field = 'pk'


    def get_object(self):
        return self.request.user

    



# from rest_framework import viewsets, permissions
# from .serializers import UserSerializer
# from django.contrib.auth import get_user_model
# from drf_spectacular.utils import extend_schema, extend_schema_view

# User = get_user_model()

# @extend_schema_view(
#     list=extend_schema(
#         summary="Lister les utilisateurs",
#         description="Récupère la liste des utilisateurs. Les Super Admins et Managers voient tous les utilisateurs, tandis que les autres ne voient que leur propre profil."
#     ),
#     retrieve=extend_schema(
#         summary="Récupérer un utilisateur spécifique",
#         description="Récupère les détails d'un utilisateur spécifique en utilisant son ID."
#     ),
#     create=extend_schema(
#         summary="Créer un nouvel utilisateur",
#         description="Crée un nouvel utilisateur. Le mot de passe doit être fourni dans le corps de la requête (champ 'password'). Ce champ n'est pas visible dans la réponse."
#     ),
#     update=extend_schema(
#         summary="Mettre à jour un utilisateur (complet)",
#         description="Met à jour complètement les informations d'un utilisateur existant en utilisant son ID."
#     ),
#     partial_update=extend_schema(
#         summary="Mettre à jour un utilisateur (partiel)",
#         description="Met à jour partiellement les informations d'un utilisateur existant en utilisant son ID."
#     ),
#     destroy=extend_schema(
#         summary="Supprimer un utilisateur",
#         description="Supprime définitivement un utilisateur de la base de données en utilisant son ID."
#     ),
# )
# @extend_schema(
#     tags=['Utilisateurs']
# )
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet pour gérer les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) sur les utilisateurs.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return User.objects.filter(id=user.id)
