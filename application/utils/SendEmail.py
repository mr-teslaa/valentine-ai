#   importing necessary module
import os
import random
import string
from flask import url_for
from flask import render_template
from flask import current_app
from flask import request
from flask_mail import Message
from application import db
from application import bcrypt
from application import mail

from application.utils.Location import getLocation

# Create an email message with an activation link
# def send_activation_email(user):
#     token = generate_otp()
#     user.activation_token = bcrypt.generate_password_hash(token).decode('utf-8')
#     db.session.commit()
#     activation_link = url_for('auth.activate_account', token=user.activation_token, _external=True)
#     msg = Message('Activate Your Account',
#                   sender=current_app.config['MAIL_DEFAULT_SENDER'],
#                   recipients=[user.email])
#     msg.html = render_template('auth/activation_email.html', activation_link=activation_link)
#     mail.send(msg)


# def send_activation_email(user):
#     otp = generate_otp()
#     print(f'====== GET THE OTP -> {otp}')
#     token = bcrypt.generate_password_hash(otp).decode('utf-8')
#     print(f'====== GET THE TOKEN -> {token}')
#     user.activation_token = token
#     print(f'====== GET THE user activation token -> {user.activation_token}')
#     db.session.commit()
#     activation_link = url_for('auth.activate_account', token=token, _external=True)
#     msg = Message('Activate Your Account',
#                   sender=current_app.config['MAIL_DEFAULT_SENDER'],
#                   recipients=[user.email])
#     msg.html = render_template('auth/activation_email.html', activation_link=activation_link)
    # mail.send(msg)

# ===================================
#     SEND ACCOUNT ACTIVATION EMAIL
# ===================================
# def send_activation_email(user):
#     token = user.generate_activation_token()
#     user.activation_token = token
#     db.session.commit()
#     activation_url = url_for('auth.activate', token=token, _external=True)
#     msg = Message('Activate Your Account - Rabeya Baten Foundation',
#                   sender=current_app.config['MAIL_DEFAULT_SENDER'],
#                   recipients=[user.email])
#     msg.html = render_template('auth/activation_link_email.html', activation_link=activation_url)
#     mail.send(msg)


# ===================================
#     SEND PASSWORD RESET EMAIL
# ===================================
def send_reset_email(user):
    token = user.get_reset_token()
    reset_link = url_for('auth.reset_token', token=token, _external=True)
    msg = Message('Password Reset Request - Valentine',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.html = render_template('auth/password_reset_link_email.html', password_reset_link=reset_link)
    mail.send(msg)


# ===================================
#     SEND EMAIL TO RECEIVER
# ===================================
def send_letter_email(letter):
    letter_link = url_for('public.letter', link=letter.link, _external=True)
    msg = Message('💌 You received a letter to read - ValentineAI',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[letter.email])
    msg.html = render_template('user/send_letter_email.html', letter_link=letter_link)
    mail.send(msg)