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

from datetime import date
from datetime import datetime

from application import db
from application.models import User
from application.models import Letter
from application.models import Visitor

from application.utils.Location import getLocation


public = Blueprint('public', __name__)

# LANDING PAGE
@public.route('/')
def index():
    # GETTING IP OF USER
    ip_request = request.remote_addr
    
    # GET TODAY
    today = datetime.utcnow().date()

    # GET VISITORS
    visitor = Visitor.query.filter_by(ip=ip_request).filter(Visitor.date_visit.like(f'{today}%')).first()

    if visitor:
        # visitor has already visited today, don't count as a new visit
        pass
    else:
        visitor = Visitor(ip=ip_request)
        db.session.add(visitor)
        db.session.commit()

    return render_template(
        'public/landing.html'
    )


# LETTER PAGE
@public.route('/letter/<string:link>/')
def letter(link):
    letter = Letter.query.filter_by(link=link).order_by(Letter.created_at.desc()).first_or_404()
    return render_template('public/letter.html', letter=letter)