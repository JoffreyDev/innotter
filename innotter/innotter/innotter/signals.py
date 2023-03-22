from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from entities.models import Page, Post
from tasks.users_tasks import send_post_notification_email

@receiver(post_save, sender=Post)
def send_email_on_new_post(sender, instance, created, **kwargs):
    if created:
        page = instance.page
        followers = page.followers.all()
        recipient_list = [follower.email for follower in followers]
        subject = f'New post on {page.name}'
        body = f'Check out the new post on {page.name}: {instance.content}'
        send_post_notification_email(recipient_list, subject, body)
        print('signal')

        