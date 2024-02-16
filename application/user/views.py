import os

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
from application.user.forms import UpdateProfileForm
from application.user.forms import UpdatePasswordForm 
from application.user.forms import LetterForm

from application.models import User
from application.models import Letter

from application.CohereAI.Utils import linkid
from application.utils.SendEmail import send_letter_email
# from application.CohereAI.GenerateBlog import generate_letter

user = Blueprint('user', __name__)

#   USER PROFILE
@user.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.user_role == 'superadmin':
        return redirect(url_for('superadmin.dashboard'))
    
    # letter = generate_letter(gender='girlfriend')

    form = LetterForm()

    if form.validate_on_submit():
        letter_link = linkid()
        
        letter = Letter(
            receiver_name=form.name.data.strip(),
            email=form.email.data.strip(),
            gender=form.gender.data,
            message=form.letter.data.strip(),
            link=letter_link,
            is_hidden=form.is_hidden.data,
            sender=current_user
        )

        db.session.add(letter)
        db.session.commit()

        send_letter_email(letter)
        flash('Message generated', 'success')
        return redirect(url_for('user.letter_sent'))

    # if request.method == 'GET':
    #     form.letter.data = letter

    return render_template(
        'user/dashboard.html', 
        title='Dashboard', 
        form=form
    )

#   USER PROFILE
# @user.route('/dashboard/letter/regenerate/', methods=['GET', 'POST'])
# @login_required
# def regenerate_message():
#     data = request.get_json()

#     gender = data['gender'] 

#     letter = generate_letter(gender)

#     res =  make_response(jsonify(letter), 200)
#     return res  


#   USER LETTERS
@user.route('/dashboard/letter/sent/', methods=['GET', 'POST'])
@login_required
def letter_sent():
    letter = Letter.query.order_by(Letter.created_at.desc()).first_or_404()
    return render_template('user/letter_sent.html', letter=letter)


#   USER PROFILE
@user.route('/dashboard/letters/', methods=['GET', 'POST'])
@login_required
def letters():
    page = request.args.get('page', 1, type=int)
    letters = Letter.query.order_by(Letter.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('user/letters.html', letters=letters)


#   USER PROFILE
@user.route('/dashboard/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        # if form.picture.data:
        #     picture_file = save_profile(form.picture.data)
        #     current_user.image_file = picture_file
        current_user.name = form.name.data.strip()
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    # image_file = url_for('static', filename='profile/' + current_user.img)
    return render_template('user/account.html', title='Profile', form=form)


#   USER PROFILE
@user.route('/dashboard/account/password/', methods=['GET', 'POST'])
@login_required
def account_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        # Get form data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_password.data
        current_password = form.current_password.data

        # Check if current password is correct
        current_password_hash = bcrypt.check_password_hash(current_user.password, current_password)
        if current_password_hash and new_password == confirm_new_password:
            # Hash and set new password
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()

        elif current_password_hash and new_password != confirm_new_password:
            flash('New Password and Confirm Password Doesn\'t Matched ⚠️', 'danger')
            return redirect(url_for('dashboard.user_profile_edit'))

        elif current_password and current_password_hash == False:
            flash('Your current password is incorrect', 'danger')
            return redirect(url_for('user.account_password'))
    
        db.session.commit()
        return redirect(url_for('user.dashboard'))

    return render_template('user/account_update_password.html', title='Password', form=form)