from celery import shared_task
import time
from management.commands.runapscheduler import my_job

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def send_notification(id_post):
    ...