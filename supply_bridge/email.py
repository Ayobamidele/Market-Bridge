from flask_mail import Message
from flask import render_template
from supply_bridge import mail, config,app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Supply Bridge] Reset Your Password',sender=config.Config.ADMINS[0],recipients=[user.email],text_body=render_template('reset_password.txt',user=user, token=token),html_body=render_template('reset-password.html',user=user, token=token))
    return token
