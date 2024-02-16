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
from wtforms.validators import Optional
from wtforms.validators import NumberRange
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

from flask_login import current_user
from application.models import User



# LETTER FORM
class LetterForm(FlaskForm):
    name = StringField(
        'Receiver Name',
        validators = [
            DataRequired(),
            Length(2, 50)
        ]
    )

    email = StringField(
        'Receiver Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )

    gender = SelectField(
        'To your',
        choices = [
            ('girlfriend', 'Girlfriend'),
            ('boyfriend', 'Boyfriend')
        ]
    )

    letter = TextAreaField(
        'Your message',
        validators = [
            DataRequired(),
            Length(10, 100)
        ]
    )

    is_hidden = BooleanField(
        'No, I don\'t want to display my name',
        validators = [DataRequired()]
    )

    submit = SubmitField('Send your surprise message')


# UPDATE PROFILE FORM
class UpdateProfileForm(FlaskForm):

    name = StringField(
        'Your Name',
        validators = [
            DataRequired(),
            Length(2, 50)
        ]
    )

    email = StringField(
        'E-mail',
        validators = [        
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
            DataRequired(),
        ]
    )

    picture = FileField(
        'Update Profile Picture', 
        validators = [
            FileAllowed(['jpg','jpeg','png'])
        ]
    )

    address = StringField(
        'Address',
        validators = [
            DataRequired(),
            Length(min=5, max=50)
        ]
    )

    submit = SubmitField('Save')

    def validate_phone(self, phone):
        if phone.data and phone.data != current_user.phone:
            user_phone = User.query.filter_by(phone=phone.data).first()
            if user_phone:
                raise ValidationError('This phone number is already registered. Please choose a different one.')

    def validate_email(self, email):
        if email.data and  email.data != current_user.email:
            user_email = User.query.filter_by(email=email.data).first()
            if user_email:
                raise ValidationError('That email is already registered. Please choose a different one.')


# UPDATE PASSWORD
class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current Password'
    )

    new_password = PasswordField(
        'New Password'
    )

    confirm_password = PasswordField(
        'Confirm New Password',
        validators = [
            DataRequired(),
            EqualTo('new_password')
        ]
    )

    submit = SubmitField('Save')
