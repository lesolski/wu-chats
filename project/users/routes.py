# project/users/routes.py

from flask import flash, redirect, url_for, request, render_template, Blueprint, current_app
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime


from project import bcrypt, db, login_manager
from project.users.forms import LogInForm, RegisterForm, RequestNewPasswordForm, NewPasswordForm
from project.users.utils import send_reg_mail, send_reset_pw_mail
from project.models import User, Group, GroupFav
from project.config import Config


serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		# getting data from form
		email = request.form['email']
		password = request.form['password']
		pw_hash = bcrypt.generate_password_hash(password)

		# DB
		existing_user = db.session.query(User).filter_by(username=email).first()

		if existing_user != None:
			if email == existing_user.username:
				flash('You already have an account, plase sign in below.', 'info')
				return redirect(url_for('users.login'))

		# this part is commented out because email is not setup yet
		# try:
		# 	send_reg_mail(email)
		# except:
		# 	flash('There was a problem on our side. Please try again later', 'info')
		# 	return render_template('signup.html', form=form)

		# adding user to DB and commiting
		new_user = User(username=email, password=pw_hash)
		db.session.add(new_user)
		db.session.commit()

		flash(f'Success! Check your email {form.email.data}, check your SPAM folder as well!', 'info')
		return redirect(url_for('users.login'))

	return render_template('signup.html', form=form)


# Route for confirming email
@users.route('/confirm_email/<token>')
def confirm_email(token):
	try:
		email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
	except:
		flash("""Bad token or your token has expired, please click <a href="/send_new_token" style="color:white; text-decoration:underline;">here</a> to resend it!""", category='alert')
		return render_template('home.html')


	user = User.query.filter_by(username=email).first_or_404()

	user.confirmed = True
	user.confirmed_on = datetime.now()

	db.session.add(user)
	db.session.commit()
	flash('Email successfully confirmed! Enjoy.', 'info')

	return redirect(url_for('users.login'))

# Route for restarting token
@users.route('/send_new_token')
@login_required
def send_new_token():
    email = current_user.username

    if email:
        try:
            send_reg_mail(email)
        except:
            flash('There was a problem on our side. Please try again later', 'info')
            return render_template('home.html')

        flash('Check your email.', 'info')
        return render_template('home.html')

    else:
        return render_template('home.html')

# Login decorator for protected views
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
	if not current_user.is_authenticated:
		flash('You must be logged in.', 'alert')
		return redirect(url_for('users.login', next=request.path))

# Login route
@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated and current_user.is_active:
		return redirect(url_for('main.home'))

	form = LogInForm()
	if form.validate_on_submit():
		if request.method == 'POST':

			email = request.form['email']
			password = request.form['password']

			user = db.session.query(User).filter_by(username=email).first()

			if user is None:
				flash("There is no account associated with this email. Register below.", "alert")
				return redirect(url_for('users.register'))

			if not bcrypt.check_password_hash(user.password, password):
				flash("Your password is wrong. Try again.", 'alert')
				return render_template('login.html', form=form)

			if bcrypt.check_password_hash(user.password, password) and email == user.username:
				login_user(user, remember=form.remember.data)
				next_page = request.args.get('next')

				if next_page:
				    flash(f'You are now logged in as {user.username}', 'info')
				    return redirect(next_page)
				else:
				    flash(f'You are now logged in as {user.username}', 'info')
				    return redirect(url_for('groups.search'))


	return render_template('login.html', form=form)

# Logout route
@users.route('/logout')
@login_required
def log_out():
	logout_user()
	flash('Successfully logged out', 'info')
	return redirect(url_for('main.home'))

# Reset Password route
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = RequestNewPasswordForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.email.data).first()
		send_reset_pw_mail(user)
		flash('An email with instructions on how to reset your password has been sent.', 'info')
		return redirect(url_for('users.login'))

	return render_template('reset_password.html', form=form)

# Reset password confirmation token route
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_pw_token(token):

	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	user = User.verify_reset_token(token)

	if user is None:
		flash('That is an invalid or expired token', 'alert')
		return redirect(url_for('users.reset_password'))

	form = NewPasswordForm()

	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = pw_hash
		db.session.commit()
		flash('Your password has been changed, you can now login with it.', 'info')
		return redirect(url_for('users.login'))

	return render_template('new_password.html', form=form)

# Profile route
@users.route('/profile/<string:username>')
@login_required
def profile(username):

	# Quarying DB for groups created and groups liked by current user
	groups_created = db.session.query(Group).filter_by(author=current_user.username).all()
	groups_liked_ids = db.session.query(GroupFav.group_id).filter_by(user_id=current_user.id)
	groups_liked = db.session.query(Group).filter(Group.id.in_(groups_liked_ids)).all()

	return render_template('profile.html', groups_created=groups_created, groups_liked=groups_liked)