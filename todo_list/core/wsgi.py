"""
WSGI config for project core.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv("MODE", "dev")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"core.settings.{environment}")

application = get_wsgi_application()
