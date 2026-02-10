from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryViewSet, ApartmentViewSet

router = DefaultRouter()
router.register(r'galleries', GalleryViewSet)
router.register(r'apartments', ApartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
