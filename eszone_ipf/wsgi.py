"""
WSGI config for eszone_ipf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eszone_ipf.settings")

import sys
import threading
from api_ipf.helpers import system_start, system_exit

sys.exitfunc = system_exit
threading.Thread(target=system_start).start()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
