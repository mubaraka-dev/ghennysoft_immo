from rest_framework import serializers
from .models import Gallery, Apartment

class ApartmentSerializer(serializers.ModelSerializer):
    gallery_name = serializers.ReadOnlyField(source='gallery.name')

    class Meta:
        model = Apartment
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True, read_only=True)
    total_apartments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Gallery
        fields = '__all__'



# Serializer pour les galeries appartenant à un utilisateur spécifique, avec le champ 'owner' en lecture seule
class UserGallerySerializer(GallerySerializer):
    class Meta(GallerySerializer.Meta):
        read_only_fields = ['owner']
        fields = '__all__'

class UserApartmentSerializer(ApartmentSerializer):
    gallery = serializers.PrimaryKeyRelatedField(queryset=Gallery.objects.all())
    class Meta(ApartmentSerializer.Meta):
        read_only_fields = ['owner']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter le choix des galeries à celles de l'utilisateur connecté
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['gallery'].queryset = Gallery.objects.filter(owner=request.user)
