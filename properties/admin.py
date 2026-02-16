from django.contrib import admin
from .models import Gallery, Apartment, GalleryManager



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



class GalleryManagerAdmin(admin.ModelAdmin):
    list_display = ('id','gallery_name','owner', 'manager_username', 'start_date', 'end_date', 'created_at')    # Champs à afficher dans la liste

    def gallery_name(self, obj):
        return obj.gallery.name if obj.gallery else "Aucune galerie"
    gallery_name.short_description = 'Nom de la galerie'

    def owner(self, obj):
        return obj.gallery.owner if obj.gallery else "Aucun propriétaire"
    owner.short_description = 'Propriétaire de la galerie'

    def manager_username(self, obj):
        return obj.manager.username if obj.manager else "Aucun manager"
    manager_username.short_description = 'Nom du manager'


admin.site.register(GalleryManager, GalleryManagerAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Apartment,ApartmentAdmin)
