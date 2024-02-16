#   importing basic flask module
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import abort
from flask import jsonify
from flask import make_response
from flask import current_app

#   importing module from flask login
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from application import db
from application import bcrypt
from application.models import User
from application.auth.forms import LoginForm 
from application.auth.forms import RegistrationForm
from application.auth.forms import UpdatePasswordForm
from application.auth.forms import ForgetPasswordForm
from application.auth.forms import ResetPasswordForm

from application.utils.SendEmail import send_reset_email

auth = Blueprint('auth', __name__)

# @auth.route('/join/admin/', methods=['GET', 'POST'])
# def join_superadmin():
#     current_ip = request.remote_addr
#     if current_user.is_authenticated:
#         current_user.ip = current_ip
#         db.session.commit()
#         return redirect(url_for('user.dashboard'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         if form.middle_name.data:
#             user = User(
#                 first_name=form.first_name.data.strip(), 
#                 middle_name=form.middle_name.data.strip(), 
#                 last_name=form.last_name.data.strip(), 
#                 phone=form.phone.data, 
#                 password=hashed_password, 
#                 email=form.email.data.strip(), address=form.address.data.strip(), 
#                 user_role='superadmin', is_active=True
#             )
#         else:
#             user = User(
#                 first_name=form.first_name.data.strip(), 
#                 last_name=form.last_name.data.strip(), 
#                 phone=form.phone.data, 
#                 password=hashed_password, 
#                 email=form.email.data.strip(), address=form.address.data.strip(), 
#                 user_role='superadmin', is_active=True
#             )
#         db.session.add(user)
#         db.session.commit()
#         send_activation_email(user)
#         send_admin_contact_alert_email(user)
#         flash('Check your email, we have sent you a confirmation link to activate your account', 'info')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/join.html', form=form)

#   NEW USER JOIN PAGE
@auth.route('/join/', methods=['GET', 'POST'])
def join():
    current_ip = request.remote_addr
    if current_user.is_authenticated:
        current_user.ip = current_ip
        db.session.commit()
        return redirect(url_for('user.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            name=form.name.data.strip(),
            phone=form.phone.data, 
            password=hashed_password, 
            email=form.email.data.strip(), 
            user_role='user', 
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/join.html', form=form)



# Activate account route
@auth.route('/activate/<token>')
def activate(token):
    # Activate a user's account
    user = User.query.filter_by(activation_token=token, is_active=False).first()
    if user:
        user_verified = user.verify_reset_token(token)
        if user_verified:
            user.is_active = True
            db.session.commit()
            flash('Your account has been activated! You are now able to log in ✅', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('The activation link is invalid or has expired.', 'warning')
        return redirect(url_for('auth.join'))


#   USER LOGIN PAGE
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    current_ip = request.remote_addr
    if current_user.is_authenticated:
        current_user.ip = current_ip
        db.session.commit()
        return redirect(url_for('user.dashboard'))

    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first_or_404()
        if user and user.is_active and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('✅ Login success', 'success')
            return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
        elif user and not user.is_active:
            flash('⚠️ Please check your email and activate your account, untill you can not login', 'info')
        else:
            flash('⚠️ Login Unsuccessful. Please check phone number and password', 'danger')
    return render_template('auth/login.html', form=form)


#   USER LOGOUT
@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('Logout successfully ✅', 'success')
    return redirect(url_for('auth.login'))


#   RESET PASSWORD FOR USER
@auth.route('/user/resetpassword/', methods=['GET', 'POST'])
@login_required
def user_resetpassword():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        newpass = form.newPassword.data
        confirmpass = form.confirmnewPassword.data
        currentpass_hash = bcrypt.check_password_hash(current_user.password, form.currentPassword.data)
        if currentpass_hash and newpass==confirmpass:
            hashed_password = bcrypt.generate_password_hash(newpass).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('user.dashboard'))
        else:
            flash('Password Not Matched', 'danger')
            return redirect(url_for('user.user_resetpassword'))

    return render_template('user/change_password.html', title='Change Password', form=form)

# VERIFY USER EMAIL IS REGISTERED IN OUR SYSTEM
@auth.route('/password/recover/', methods=['GET', 'POST'])
def forgetpassword():
    form = ForgetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('If you have an account with this email, an email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/forgetpassword.html', title='Reset Password', form=form)


#   PASSWORD RESET TOKEN
@auth.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)