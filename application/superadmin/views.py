import os
from datetime import datetime
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
from sqlalchemy import func
#   importing module from flask login
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from application import db
from application import bcrypt
# from application.superadmin.forms import aksjdlkf

from application.models import User

from application.utils.Utils import applicationID
from application.utils.CutomAuth import superadmin_required

superadmin = Blueprint('superadmin', __name__)

#   USER PROFILE
@superadmin.route('/superadmin/dashboard/', methods=['GET', 'POST'])
@login_required
@superadmin_required
def superadmin_dashboard():

    return render_template(
        'superadmin/dashboard.html', 
        title='Admin Dashboard',
    )