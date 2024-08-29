from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_reset_email_task(email, reset_link):
    try:
        subject = 'Password Reset Request'
        html_message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
        
        send_mail(
            subject,
            strip_tags(html_message),
            settings.EMAIL_HOST,
            [email],
        )
    except Exception as e:
        print("Error sending email: ", e)
