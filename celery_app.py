from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Встановлюємо стандартний settings модуль для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRTR.settings')

# Створюємо інстанс Celery
app = Celery('HRTR')

# Завантажуємо конфігурацію Celery з файлу Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично відкриваємо всі таски в проекті (забезпечує реєстрацію)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
