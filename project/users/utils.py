# project/users/utils.py

from flask import url_for, render_template, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from project import mail



def send_reg_mail(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    link = url_for('users.confirm_email', token=token, _external=True)
    msg = Message(subject='Email Confirmation, WU Student community', sender='office@wu-community.com', recipients=[email])
    msg.html = render_template('mails/mail.html', link=link)
    mail.send(msg)


def send_reset_pw_mail(user):
	token = user.get_reset_token()
	msg = Message('Reset your password',
				sender='office@wu-community.com',
				recipients=[user.username])

	link = url_for('users.reset_pw_token', token=token, _external=True)
	msg.html = render_template('mails/mail_reset_password.html', link=link)
	mail.send(msg)





