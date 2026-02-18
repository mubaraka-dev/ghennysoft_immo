#!/bin/bash
# Script pour exécuter la commande process_rents Django

# Aller dans le dossier du projet
cd /home/mubaraka/Bureau/GhennySoft/backend_ghennysoft_network/backend

# Activer le virtualenv
source env/bin/activate

# Exécuter la commande Django
python manage.py process_rents
