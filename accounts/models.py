from django.contrib.auth.models import AbstractUser
from django.db import models

class UserChoice(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    MANAGER = 'MANAGER', 'Manager'
    ACCOUNTANT = 'ACCOUNTANT', 'Comptable'
    CONCIERGE = 'CONCIERGE', 'Concierge'
    TENANT = 'TENANT', 'Locataire'
    

class User(AbstractUser):
    
    role = models.CharField(max_length=20, choices=UserChoice.choices, default=UserChoice.TENANT)

    def __str__(self):
        return f"{self.username} ({self.role})"
