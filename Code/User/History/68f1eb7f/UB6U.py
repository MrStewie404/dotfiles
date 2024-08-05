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
def send_wekly_notification(subscribers, preview, pk, title):
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