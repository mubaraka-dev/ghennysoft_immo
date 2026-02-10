from rest_framework import serializers
from .models import Gallery, Apartment

class ApartmentSerializer(serializers.ModelSerializer):
    gallery_name = serializers.ReadOnlyField(source='gallery.name')

    class Meta:
        model = Apartment
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True, read_only=True)
    total_apartments = serializers.IntegerField(source='apartments.count', read_only=True)

    class Meta:
        model = Gallery
        fields = '__all__'
