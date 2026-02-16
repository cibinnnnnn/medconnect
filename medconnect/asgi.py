"""
ASGI config for MedConnect project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medconnect.settings')

application = get_asgi_application()
