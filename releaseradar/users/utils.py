import flask
import flask_mail
from releaseradar import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = flask_mail.Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{flask.url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, you can safely ignore this email.
'''
    mail.send(msg)
