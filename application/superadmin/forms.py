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


# FUNDS ANALYTICS DATE RANGE
# class FundsAnalyticsDateRangeForm(FlaskForm):
#     submit = SubmitField('Submit')