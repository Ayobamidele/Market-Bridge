from flask_mail import Message
from flask import render_template
from api import mail
from threading import Thread

from api.utils import config

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    print(msg)
    mail.send(msg)
    
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Supply Bridge] Reset Your Password',sender=config.Config.ADMINS[0],recipients=[user.email],text_body=render_template('auth/password/reset_password.txt',user=user, token=token),html_body=render_template('auth/password/reset-password.html',user=user, token=token))
    return token
