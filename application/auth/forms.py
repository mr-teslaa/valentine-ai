from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import IntegerField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms import DateField

from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed

from wtforms.validators import DataRequired
from wtforms.validators import NumberRange
from wtforms.validators import Optional
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from flask_login import current_user
from application.models import User

class RegistrationForm(FlaskForm):
    name = StringField(
        'Your Name',
        validators = [
            DataRequired(),
            Length(2, 50)
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Length(min=5, max=15, message='Phone number must be between 5 and 15.')
        ]
    )

    email = StringField(
        'E-mail',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Password',
        validators = [ DataRequired() ]
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )

    submit = SubmitField('Join Now')
    
    def validate_phone(self, phone):
        user_phone = User.query.filter_by(phone=phone.data).first()
        if user_phone:
            raise ValidationError('This Phone is alredy registerd. Please choose a different one.')

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('That email is taken/already registered. Please choose a different one.')
            


class LoginForm(FlaskForm):
    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
            Length(min=5, max=15, message='Phone number must be between 5 and 15.')
        ]
    )

    password = PasswordField(
        'Password', 
        validators = [DataRequired()]
    )

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


# UPDATE PASSWORD FORM
class UpdatePasswordForm(FlaskForm):
    currentPassword = PasswordField(
        'Current Password', 
        validators=[ DataRequired() ]
    )

    newPassword = PasswordField(
        'New Password', 
        # validators=[ DataRequired() ]
    )

    confirmnewPassword = PasswordField(
        'Confirm New Password', 
        # validators=[ DataRequired() ]
    )

    submit = SubmitField('Save')


#   FORGET PASSWORD FORM
class ForgetPasswordForm(FlaskForm):
    email = StringField(
        'Email',
        validators = [
            Email()
        ]
    )

    submit = SubmitField('Get Password Reset Link')


#   CHANGE PASSWORD TOKEN
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
            'Password',
            validators=[ DataRequired() ]
    )

    confirm_password = PasswordField(
            'Confirm Password',
            validators = [
                DataRequired(),
                EqualTo('password')
            ]
    )

    submit = SubmitField('Reset Password')