from django.contrib import admin
from .models import Gallery, Apartment



class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'owner', 'address', 'contact_info', 'created_at')    # Champs à afficher dans la liste
    
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id','number', 'gallery_name', 'proprietaire_gallery','status', 'created_at')    # Champs à afficher dans la liste

    def gallery_name(self, obj):
        return obj.gallery.name if obj.gallery else "Aucune galerie"
    gallery_name.short_description = 'Nom de la galerie'

    def proprietaire_gallery(self, obj):
        return obj.gallery.owner if obj.gallery else "Aucun propriétaire"
    proprietaire_gallery.short_description = 'Propriétaire de la galerie'

admin.site.register(Gallery,GalleryAdmin)
admin.site.register(Apartment,ApartmentAdmin)
