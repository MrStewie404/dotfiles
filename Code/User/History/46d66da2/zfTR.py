from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from .tasks import send_wekly_notification
from project.settings import SITE_URL
# from project import settings

from .models import PostCategory, Subscription


# def send_notification(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{SITE_URL}/{pk}'
#         }
#         )
#     msg = EmailMultiAlternatives(
#         subject=title,  
#         body='',  
#         from_email=settings.DEFAULT_FROM_EMAIL,  
#         to=subscribers
#     )

#     print(msg)
#     msg.attach_alternative(html_content,  "text/html")
#     msg.send()
#     print("\n"*10+"Message send!")


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += Subscription.objects.filter(category=category).values_list('user__email', flat=True)
        subscribers = set(subscribers)

        print("==="*20+"\nСоздана новость!\n"+"==="*20)
        print(f"{kwargs}")
        signal, action, model, pk_set = kwargs
        print(model)

        send_wekly_notification(instance, preview, pk, title, subscribers)