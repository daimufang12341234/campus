"""
WSGI config for campus_life project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_life.settings')

application = get_wsgi_application() 