from django.contrib import admin
from .models import  Contract,Rent, Payment, SupplierInvoice

class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner','tenant', 'apartment', 'start_date', 'end_date', 'rent_amount', 'archive_at')
    search_fields = ('tenant__first_name', 'tenant__last_name', 'apartment__number')
    list_filter = ('start_date', 'end_date')

admin.site.register(Contract, ContractAdmin)
admin.site.register(Rent)
admin.site.register(Payment)
admin.site.register(SupplierInvoice)
