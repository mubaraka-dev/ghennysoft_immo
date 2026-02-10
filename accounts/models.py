from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('MANAGER', 'Manager'),
        ('ACCOUNTANT', 'Comptable'),
        ('CONCIERGE', 'Concierge'),
        ('TENANT', 'Locataire'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TENANT')

    def __str__(self):
        return f"{self.username} ({self.role})"
