import secrets
#   importing  necessary module
from datetime import datetime
from flask import current_app

#   importing dataase
from application import db

#   importing login manager
from application import login_manager
from flask_login import UserMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


#   making sure that the user is logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    phone = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(120), unique=True)
    img = db.Column(db.String(500), default='default.jpg')
    password = db.Column(db.String(800), nullable=False)
    address = db.Column(db.String(900))
    user_role = db.Column(db.String(60), default="user")
    letter_sender = db.relationship('Letter', backref='sender', lazy=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip = db.Column(db.String(60))
    # ACCOUNT ACTIVATION
    activation_token = db.Column(db.String(500), unique=True)
    is_active = db.Column(db.Boolean(), default=False)

    # GENERATE ACTIVATION TOKEN
    def generate_activation_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    #   GENERATING PASSWORD RESET TOKEN
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    #  verify the token if the token has exprired or invalid
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    #  verify the token if the token has exprired or invalid
    @staticmethod
    def verify_activation_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiver_name = db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)
    gender=db.Column(db.String(100), nullable=False)
    message=db.Column(db.String(900))
    link=db.Column(db.String(100), unique=True)
    is_hidden = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), nullable=False)
    first_name=db.Column(db.String(100))
    middle_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    phone=db.Column(db.String(100))
    message=db.Column(db.String(100))
    date_visit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
