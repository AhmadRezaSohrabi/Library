import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "borrow_daily_fee_collection": {
        "task": "borrow_daily_fee_collection",
        "schedule": crontab(hour="1") # Run at 1 UTC or almost 9 am(in Tehran/Asia)
    },
    "calculate_category_income": {
        "task": "calculate_category_income",
        'schedule': crontab(hour='*/6') # Run every 6 hours
    },
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
