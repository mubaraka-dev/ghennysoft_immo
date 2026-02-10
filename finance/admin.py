from django.contrib import admin
from .models import Rent, Payment, SupplierInvoice

admin.site.register(Rent)
admin.site.register(Payment)
admin.site.register(SupplierInvoice)
