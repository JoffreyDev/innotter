from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from entities.models import Page, Post
from tasks.users_tasks import send_post_notification_email
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from services.statistics_service import send_user_id_to_rabbitmq

@receiver(post_save, sender=Post)
def send_email_on_new_post(sender, instance, created, **kwargs):
    if created:
        page = instance.page
        followers = page.followers.all()
        recipient_list = [follower.email for follower in followers]
        subject = f'New post on {page.name}'
        body = f'Check out the new post on {page.name}: {instance.content}'
        send_post_notification_email(recipient_list, subject, body)
    send_user_id_to_rabbitmq(sender, instance.page.owner, **kwargs)

@receiver(post_save, sender=Page)
def trigger_statistics_collection(sender, instance, created, **kwargs):
    send_user_id_to_rabbitmq(sender, instance.owner, **kwargs)
