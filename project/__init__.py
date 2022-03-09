# project/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from project.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app(config_class=Config):

	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# blueprints imports 
	from project.users.routes import users
	from project.groups.routes import groups
	from project.main.routes import main
	from project.errors.error_handlers import errors

	# register blueprints
	app.register_blueprint(users)
	app.register_blueprint(groups)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	
	return app