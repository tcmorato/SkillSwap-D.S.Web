"""
WSGI config for tulio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tulio.settings')

from django.core.wsgi import get_wsgi_application
from servestatic import ServeStatic
from django.conf import settings

application = get_wsgi_application()
application = ServeStatic(application)
application.add_files(settings.MEDIA_ROOT, settings.MEDIA_URL)