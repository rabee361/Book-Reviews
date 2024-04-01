import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookpro.settings')

app = Celery('Bookpro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


