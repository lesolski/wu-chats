# project/models.py

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from project import db

class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	password = db.Column(db.String(60))
	confirmed = db.Column(db.Boolean, default=False)
	confirmed_on = db.Column(db.DateTime, default=None)


	def is_active(self):
		if self.confirmed == True:
			return True
		else:
			return False

    # Authentication
	def get_reset_token(self, expires_in_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_in_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	# Favorites
	faved = db.relationship(
		'GroupFav',
		foreign_keys='GroupFav.user_id',
		backref='user', lazy='dynamic')

	def like_group(self, group):
		if not self.has_liked_group(group):
			like = GroupFav(user_id=self.id, group_id=group.id)
			db.session.add(like)

	def unlike_group(self, group):
		if self.has_liked_group(group):
			GroupFav.query.filter_by(
			user_id=self.id,
			group_id=group.id).delete()

	def has_liked_group(self, group):
		return GroupFav.query.filter(
			GroupFav.user_id == self.id,
			GroupFav.group_id == group.id).count() > 0


class GroupFav(db.Model):

	__tablename__ = 'group_fav'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))



class Group(db.Model):

	__tablename__ = "groups"

	id = db.Column(db.Integer, primary_key=True)
	semester = db.Column(db.String(4))
	group_name = db.Column(db.String(300))
	course_id = db.Column(db.String(6))
	professors = db.Column(db.String(300))
	platform = db.Column(db.String(300))
	group_link = db.Column(db.String(300))
	show_admin = db.Column(db.Integer)
	author = db.Column(db.String(50), db.ForeignKey('users.username'))
	qr_code = db.Column(db.Text)

	favs = db.relationship('GroupFav', backref='group', lazy='dynamic')


class FAQs(db.Model):

	__tablename__ = "faqs"

	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String)
	answer = db.Column(db.String)


class News(db.Model):

	__tablename__ = "news"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	descr = db.Column(db.String)
	link = db.Column(db.String)
	published_at = db.Column(db.String)