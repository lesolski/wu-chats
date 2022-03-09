# project/users/forms.py

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, InputRequired, Length

from project import db
from project.models import User

class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "WU Email (@s.wu.ac.at)"})
	password = PasswordField('Password', validators=[InputRequired(), DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
	password2 = PasswordField('Repeat your Password', validators=[InputRequired(), DataRequired(), EqualTo('password', message="Passwords don't match. Please try again.")],
	render_kw={"placeholder": "Repeat your password"})
	recaptcha = RecaptchaField()
	submit = SubmitField('REGISTER')

	def validate_email(self, field):
		if field.data[-11:] != '@s.wu.ac.at':
			raise ValidationError('You can only register with WU student email (@s.wu.ac.at)')

class LogInForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), DataRequired()],render_kw={"placeholder": "WU Email (@s.wu.ac.at)"})
	password = PasswordField('password', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "Password"})
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

	def validate_email(self, field):
		if field.data[-11:] != '@s.wu.ac.at':
			raise ValidationError('You can only login with WU student email (@s.wu.ac.at)')


class RequestNewPasswordForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "WU Email (@s.wu.ac.at)"})
	submit = SubmitField('Request New Password')

	def validate_email(self, field):
		if not db.session.query(User).filter_by(username=field.data).first():
			raise ValidationError('There is no registered user with this email.')


class NewPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "Password"})
	password2 = PasswordField('Repeat your Password', validators=[InputRequired(), DataRequired(), EqualTo('password', message="Passwords don't match. Please try again.")],
	render_kw={"placeholder": "Repeat your password"})
	submit = SubmitField('Reset Password')