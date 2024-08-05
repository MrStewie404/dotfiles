from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from project.settings import SITE_URL
from .models import Subscription
from celery import shared_task
from project import settings
import time


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def send_subs_notification(subscribers, preview, pk, title):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/{pk}'
        }
        )
    msg = EmailMultiAlternatives(
        subject=title,  
        body='',  
        from_email=settings.DEFAULT_FROM_EMAIL,  
        to=subscribers
    )
    
    msg.attach_alternative(html_content,  "text/html")
    msg.send()
    print("\n"*10+"Message send!")


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