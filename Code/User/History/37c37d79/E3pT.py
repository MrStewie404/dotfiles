import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
 
app = Celery('project')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.management.commands.runapscheduler.my_job',
        'schedule': crontab(hour=13, minute=4, day_of_week='Sunday'),
    },
}




# Command for run tasks:
# celery -A project worker -l INFO -B