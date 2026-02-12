from django.db import models
from tenants.models import Contract
from properties.models import Gallery, Apartment


class RentStatusChoices(models.TextChoices):
    UNPAID = 'UNPAID', 'Non Payé'
    PAID = 'PAID', 'Payé'
    LATE = 'LATE', 'En Retard'
    PARTIAL = 'PARTIAL', 'Partiellement Payé'

class Rent(models.Model):
    

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='rents')
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=RentStatusChoices.choices, default=RentStatusChoices.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loyer {self.contract.tenant} - {self.period_start}"

    @property
    def total_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance(self):
        return self.amount - self.total_paid

class METHOD_CHOICES(models.TextChoices):
    CASH = 'CASH', 'Espèces'
    BANK = 'BANK', 'Virement Bancaire'
    MOBILE_MONEY = 'MOBILE_MONEY', 'Mobile Money'
    CHECK = 'CHECK', 'Chèque'
class Payment(models.Model):
    

    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default=METHOD_CHOICES.CASH)
    reference = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.amount} - {self.rent}"



class  PROVIDER_CHOICES(models.TextChoices):
    SNEL = 'SNEL', 'SNEL'
    REGIDESO = 'REGIDESO', 'REGIDESO'
    OTHER = 'OTHER', 'Autre'

class InvoiceStatusChoices(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    PAID = 'PAID', 'Payé'

class SupplierInvoice(models.Model):

    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, default=PROVIDER_CHOICES.OTHER)
    reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=InvoiceStatusChoices.choices, default=InvoiceStatusChoices.PENDING)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture {self.provider} - {self.amount}"
