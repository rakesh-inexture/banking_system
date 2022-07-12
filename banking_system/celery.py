from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banking_system.settings")

app = Celery('banking_system')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#celery beat is a scheduler; It kicks off tasks at regular intervals.
app.conf.beat_schedule = {
    # Executes 1st day of every Month.
    'every-minute': {
        'task': 'count_interest',
        # crontab can be changes to change Schedule
        # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
        # 'schedule': crontab(0, 0, day_of_month='1'),
        'schedule': crontab(minute='1'),
    }
}
@app.task(bind=True)
def debug_task(self):
    # print(f"Request: {self.request!r}")
    print('Request: {0!r}'.format(self.request))
