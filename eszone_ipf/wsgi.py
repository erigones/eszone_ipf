"""
WSGI config for eszone_ipf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import threading
from eszone_ipf.helpers import system_start

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eszone_ipf.settings")
#threading.Thread(target=system_start).start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()