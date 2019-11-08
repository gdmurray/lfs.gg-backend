from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

if os.environ.get("DJANGO_ENVIRONMENT", None) == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lfsgg.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lfsgg.settings')

from django.apps import apps

app = Celery('lfsgg')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
