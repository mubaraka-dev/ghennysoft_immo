from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GalleryList, ApartmentList, UserGalleryViewSet, UserApartmentViewSet, GalleryManagerViewSet

router = DefaultRouter()
router.register(r'galleries', GalleryList)
router.register(r'my-galleries', UserGalleryViewSet, basename='my-gallery')
router.register(r'apartments', ApartmentList)
router.register(r'my-apartments', UserApartmentViewSet, basename='my-apartment')
router.register(r'gallery-managers', GalleryManagerViewSet, basename='gallery-manager')

urlpatterns = [
    path('', include(router.urls)),
]
