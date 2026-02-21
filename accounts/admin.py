from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
class UserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username'] 
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ( 'adress')}),
    # )

admin.site.register(User, UserAdmin)
