from django.core.mail import send_mail
from applications.notifications.models import ContactSuv
from rent.celery import app


@app.task
def send_new_client():
    msg = f'Привет! Появилось новое объявление для внедорожников'
    for i in ContactSuv.objects.all():
        send_mail(
            'From cars rent',
            msg,
            'csqvsr25@gmail.com',
            [i.email]
        )