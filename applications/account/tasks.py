from django.core.mail import send_mail

from rent.celery import app
my_email = 'csqvsr25@gmail.com'


@app.task
def send_confirmation_email(code, email):
    link = f'Спасибо за регистрацию! \nДля активации вашего аккаунта перейдите по ссылке: '\
           f'http://localhost:8000/api/v1/account/active/{code}'

    send_mail(
        'From cars rent',
        link,
        'my_email',
        [email]
    )

@app.task
def send_code_recovery(code, email):
    send_mail(
        'Восстановление пароля',
        f'Ваш код подтверждения: {code}',
        my_email,
        [email]
    )