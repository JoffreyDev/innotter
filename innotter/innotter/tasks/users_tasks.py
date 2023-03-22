from celery import shared_task
from services.mail_service import send_email

@shared_task
def send_post_notification_email(user_email, subject, body):
    send_email(subject, body, user_email)
    print('task')

    