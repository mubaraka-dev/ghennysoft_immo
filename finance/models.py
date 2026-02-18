from django.db import models
from properties.models import Gallery, Apartment
from accounts.models import User
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Contract(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractOwner')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractTenant')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='contractAppartement')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    archive_at = models.DateTimeField(blank=True, null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrat {self.tenant} - {self.apartment}"


class RentStatusChoices(models.TextChoices):
    UNPAID = 'UNPAID', 'Non Payé'
    PAID = 'PAID', 'Payé'
    LATE = 'LATE', 'En Retard'
    PARTIAL = 'PARTIAL', 'Partiellement Payé'

class Rent(models.Model):
    
    # Relation avec le contrat de location. Chaque loyer est lié à un contrat.
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='rents')
    # Date de début de la période pour laquelle le loyer est dû.
    period_start = models.DateField()
    # Date de fin de la période pour laquelle le loyer est dû.
    period_end = models.DateField()
    # Date à laquelle le paiement du loyer est attendu.
    due_date = models.DateField()
    # Montant total du loyer pour la période.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Statut actuel du loyer (par exemple, Non Payé, Payé, En Retard).
    status = models.CharField(max_length=20, choices=RentStatusChoices.choices, default=RentStatusChoices.UNPAID)
    # Horodatage de la création de l'enregistrement de loyer.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Fournit une représentation textuelle lisible pour chaque objet Loyer.
        return f"Loyer {self.contract.tenant} - {self.period_start}"

    @property
    def total_paid(self):
        # Calcule et retourne la somme de tous les paiements effectués pour ce loyer.
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance(self):
        # Calcule le solde restant en soustrayant le total payé du montant du loyer.
        return self.amount - self.total_paid
    
    @classmethod
    def process_rents(cls):
        # Méthode de classe pour générer automatiquement les loyers pour la période suivante.
        today = timezone.now().date()

        # Récupère tous les loyers existants pour les traiter.
        rents = cls.objects.select_related("contract").all()

        for rent in rents:
            # Passe au loyer suivant si la date de fin de période n'est pas définie.
            if not rent.period_end:
                continue

            # Passe au loyer suivant si la période de location actuelle n'est pas encore terminée.
            if today <= rent.period_end:
                continue

            with transaction.atomic():
                # Calcule les dates de début et de fin pour la prochaine période de loyer.
                next_start = rent.period_start + relativedelta(months=1)
                next_end = next_start + relativedelta(months=1) - timedelta(days=1)

                # Vérifie si un loyer pour la période suivante existe déjà pour éviter les doublons.
                exists = cls.objects.filter(
                    contract=rent.contract,
                    period_start=next_start
                ).exists()

                # Si le loyer pour la période suivante n'existe pas, il est créé.
                if not exists:
                    cls.objects.create(
                        contract=rent.contract,
                        period_start=next_start,
                        period_end=next_end,
                        due_date=next_start,
                        amount=rent.amount,
                        status=RentStatusChoices.UNPAID
                    )


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
from django.db import models
from properties.models import Gallery, Apartment
from accounts.models import User
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Contract(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractOwner')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contractTenant')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='contractAppartement')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    archive_at = models.DateTimeField(blank=True, null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrat {self.tenant} - {self.apartment}"


class RentStatusChoices(models.TextChoices):
    UNPAID = 'UNPAID', 'Non Payé'
    PAID = 'PAID', 'Payé'
    LATE = 'LATE', 'En Retard'
    PARTIAL = 'PARTIAL', 'Partiellement Payé'

class Rent(models.Model):
    
    # Relation avec le contrat de location. Chaque loyer est lié à un contrat.
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='rents')
    # Date de début de la période pour laquelle le loyer est dû.
    period_start = models.DateField()
    # Date de fin de la période pour laquelle le loyer est dû.
    period_end = models.DateField()
    # Date à laquelle le paiement du loyer est attendu.
    due_date = models.DateField()
    # Montant total du loyer pour la période.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Statut actuel du loyer (par exemple, Non Payé, Payé, En Retard).
    status = models.CharField(max_length=20, choices=RentStatusChoices.choices, default=RentStatusChoices.UNPAID)
    # Horodatage de la création de l'enregistrement de loyer.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Fournit une représentation textuelle lisible pour chaque objet Loyer.
        return f"Loyer {self.contract.tenant} - {self.period_start}"

    @property
    def total_paid(self):
        # Calcule et retourne la somme de tous les paiements effectués pour ce loyer.
        return sum(payment.amount for payment in self.payments.all())

    @property
    def balance(self):
        # Calcule le solde restant en soustrayant le total payé du montant du loyer.
        return self.amount - self.total_paid
    
    @classmethod
    def process_rents(cls):
        # Méthode de classe pour générer automatiquement les loyers pour la période suivante.
        today = timezone.now().date()

        # Récupère tous les loyers existants pour les traiter.
        rents = cls.objects.select_related("contract").all()

        for rent in rents:
            # Passe au loyer suivant si la date de fin de période n'est pas définie.
            if not rent.period_end:
                continue

            # Passe au loyer suivant si la période de location actuelle n'est pas encore terminée.
            if today <= rent.period_end:
                continue

            with transaction.atomic():
                # Calcule les dates de début et de fin pour la prochaine période de loyer.
                next_start = rent.period_start + relativedelta(months=1)
                next_end = next_start + relativedelta(months=1) - timedelta(days=1)

                # Vérifie si un loyer pour la période suivante existe déjà pour éviter les doublons.
                exists = cls.objects.filter(
                    contract=rent.contract,
                    period_start=next_start
                ).exists()

                # Si le loyer pour la période suivante n'existe pas, il est créé.
                if not exists:
                    cls.objects.create(
                        contract=rent.contract,
                        period_start=next_start,
                        period_end=next_end,
                        due_date=next_start,
                        amount=rent.amount,
                        status=RentStatusChoices.UNPAID
                    )


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

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour mettre à jour le statut du loyer associé
        après chaque enregistrement ou mise à jour de paiement.
        """
        # On sauvegarde d'abord l'objet paiement lui-même.
        super().save(*args, **kwargs)
        
        rent = self.rent
        # On met à jour le statut du loyer en fonction du nouveau solde.
        # Les propriétés `total_paid` et `balance` sont recalculées à la volée.
        if rent.balance <= 0:
            rent.status = RentStatusChoices.PAID
        elif rent.total_paid > 0:
            rent.status = RentStatusChoices.PARTIAL
        else:
            rent.status = RentStatusChoices.UNPAID
        rent.save()

    # la suppression des paiements est interdite pour des raisons de sécurité, afin de garantir l'intégrité des données financières.
    def delete(self, *args, **kwargs):
        raise NotImplementedError("La suppression des paiements n'est pas autorisée pour des raisons de sécurité.")



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
