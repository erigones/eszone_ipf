"""
WSGI config for eszone_ipf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
from eszone_ipf.helpers import start

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eszone_ipf.settings")
start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()