from getpass import getpass

class Config:

	# DB CONFIG
	SQLALCHEMY_DATABASE_URI = 'sqlite://///home/lesol/projects/wu-chats/project/data/db.sqlite3'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# SECRETS CONFIG
	SECRET_KEY = '1secretkeybrosk1mojdobri'
	SECURITY_PASSWORD_SALT = 'malosoliljubitebrat'
	SALT = 'confirm-email'

	# MAIL CONFIG
	MAIL_SERVER = 'smtp.office365.com'
	MAIL_PORT = 587
	MAIL_USERNAME = 'office@wu-community.com'
	MAIL_PASSWORD = getpass(prompt='Email password: ')
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_DEFAULT_SENDER = 'office@wu-community.com'
	MAIL_MAX_EMAILS = 5
	MAIL_ASCII_ATTACHMENTS = False
	RECAPTCHA_USE_SSL = False
	RECAPTCHA_PUBLIC_KEY ='USE YOUR KEYS'
	RECAPTCHA_PRIVATE_KEY = 'USE YOUR KEYS'
	RECAPTCHA_OPTIONS = {'theme':'black'}
