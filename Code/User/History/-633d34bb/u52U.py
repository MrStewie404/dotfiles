import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import mail_managers
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from project.settings import SITE_URL
import datetime
from news.models import Post, Subscription


logger = logging.getLogger(__name__)


def send_weekly_news():
    today = datetime.datetime.today()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime__gte=last_week)
    categories = set(posts.values_list('category__id', flat=True))
    subscribers = set(Subscription.objects.filter(category_id__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string(
            'weekly_newsletter.html',
            {
                'link': f'{SITE_URL}',
                'posts': posts
            }
        )
    
    msg = EmailMultiAlternatives(
        subject='Новости за последнюю неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` 
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.
  
    :param max_age: The maximum length of time to retain historical 
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                    #second="*/1",
                    day_of_week="fri", 
                    hour="18", 
                    minute="00"
                ),  # Every Friday in 18:00
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="10"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")