from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from application.config import Config

from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()
mail = Mail()

login_manager.login_view = 'auth.login'

login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from application.models import User
    from application.models import Visitor

    from application.auth.views import auth
    app.register_blueprint(auth)
    
    from application.public.views import public
    app.register_blueprint(public)
    
    from application.superadmin.views import superadmin
    app.register_blueprint(superadmin)

    from application.user.views import user
    app.register_blueprint(user)

    return app