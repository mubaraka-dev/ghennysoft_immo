import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghenny_soft_immo.settings')

application = get_wsgi_application()
