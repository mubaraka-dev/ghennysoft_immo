from django.core.management.base import BaseCommand
from finance.models import Rent  # ton modèle Rent

class Command(BaseCommand):
    help = "Process and generate monthly rents"

    def handle(self, *args, **kwargs):
        Rent.process_rents()
        self.stdout.write(self.style.SUCCESS("Rents processed successfully"))
