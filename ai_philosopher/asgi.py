"""
ASGI config for ai_philosopher project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_philosopher.settings')

application = get_asgi_application()
