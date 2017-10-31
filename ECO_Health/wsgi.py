"""
WSGI config for ECO_Health project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECO_Health.settings")

application = get_wsgi_application()

sys.path.append('C:/Users/gzhang/Desktop/ECO_Health')