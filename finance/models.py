from django.db import models
from tenants.models import Contract
from properties.models import Gallery, Apartment

class Rent(models.Model):
    STATUS_CHOICES = (
        ('UNPAID', 'Impayé'),
        ('PARTIAL', 'Partiel'),
        ('PAID', 'Payé'),
        ('LATE', 'En retard'),
    )

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='rents')
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loyer {self.contract.tenant} - {self.period_start}"

    @property
    def total_paid(self):
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance(self):
        return self.amount - self.total_paid

class Payment(models.Model):
    METHOD_CHOICES = (
        ('CASH', 'Espèces'),
        ('BANK_TRANSFER', 'Virement Bancaire'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CHECK', 'Chèque'),
    )

    rent = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='CASH')
    reference = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.amount} - {self.rent}"

class SupplierInvoice(models.Model):
    PROVIDER_CHOICES = (
        ('SNEL', 'SNEL'),
        ('REGIDESO', 'REGIDESO'),
        ('OTHER', 'Autre'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
    )

    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='invoices', blank=True, null=True)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture {self.provider} - {self.amount}"
