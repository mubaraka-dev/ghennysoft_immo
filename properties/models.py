from django.db import models

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class STATUS_CHOICES(models.TextChoices):
    FREE = 'FREE', 'Libre'
    OCCUPIED = 'OCCUPIED', 'Occupé'
    MAINTENANCE = 'MAINTENANCE', 'En maintenance'
class Apartment(models.Model):

    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='apartments')
    number = models.CharField(max_length=50)
    type = models.CharField(max_length=100, help_text="Studio, F1, F2, etc.")
    floor = models.CharField(max_length=50, blank=True, null=True)
    surface = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="m2")
    standard_rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES.FREE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.number} - {self.gallery.name}"
