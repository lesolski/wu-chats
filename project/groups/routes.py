# project/groups/routes.py

from functools import wraps

from flask import render_template, request, redirect, url_for, flash, Blueprint, Markup
from flask_login import login_required, current_user

from project import db
from project.models import Group
from project.groups.forms import SearchForm, AddGroupForm
from project.groups.utils import make_qr_code

groups = Blueprint('groups', __name__)

# Decorator that prevents users to access certain pages if they didn't confirm email
def confirmed_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_active():
            flash(Markup("""You must confirm your email to see this page. You can request new confirmation email <a href="/send_new_token" style="color:white; text-decoration:underline;>here</a>"""), category='alert')
            return redirect(url_for('main.home', next=request.path))
        return func(*args, **kwargs)
    return decorated_view

# Search Chats/Groups route
@groups.route('/search', methods=['GET', 'POST'])
@login_required
@confirmed_required
def search():

	form = SearchForm()

	if request.args.get('search'):

		page = request.args.get('page', 1, type=int)
		asked = request.args.get("search")

		try:
			asked = int(asked)
		except:
			pass
		# Search DB and Pagination
		if not isinstance(asked, int):
			search = "%{}%".format(asked)
			groups = Group.query.filter(Group.group_name.like(search)).order_by(Group.id.desc()).paginate(page=page, per_page=15)

		else:
			groups = Group.query.filter(Group.course_id == asked).order_by(Group.id.desc()).paginate(page=page, per_page=15)

		if len(groups.items) > 0:
			return render_template('search.html', groups=groups, form=form)
		else:
			flash("We didn't find anything similar with that course name or course ID, try again.", 'alert')
			return redirect(url_for('groups.search'))

	else:
		page = request.args.get('page', 1, type=int)
		groups = Group.query.order_by(Group.id.desc()).paginate(page=page, per_page=15)
		return render_template('search.html', form=form, groups=groups)



# Route for adding new group
@groups.route('/add', methods=['GET', 'POST'])
@login_required
@confirmed_required
def add():
	
	form = AddGroupForm()

	if current_user.is_active:
		if form.validate_on_submit() and request.method == 'POST':


			if request.form['platform'] == 'WhatsApp':
			    qr_code = make_qr_code(request.form['grouplink'], '#25D366')

			elif request.form['platform'] == 'Telegram':
			    qr_code = make_qr_code(request.form['grouplink'], '#0088cc')

			# New SQLAlchemy Group Object
			new_group = Group(semester = request.form['semester'],
							group_name = request.form['group_name'],
							course_id = request.form['course_id'],
							professors = request.form['professors'],
							platform = request.form['platform'],
							group_link = request.form['grouplink'],
							show_admin = request.form['show_admin'],
							author = current_user.username,
							qr_code = qr_code
							)
			# Add to DB and commit
			db.session.add(new_group)
			db.session.commit()
			flash(f"Your group for course with ID {request.form['course_id']}  was added.", 'info')
			return redirect(url_for('groups.add'))
		else:
			return render_template('add.html', form=form)


	flash('You need to confirm your email to be able to post new groups.', 'alert')
	return render_template('add.html', form=AddGroupForm())


# Like function
@groups.route('/like/<int:group_id>/<action>')
@login_required
@confirmed_required
def like_action(group_id, action):

    group = Group.query.filter_by(id=group_id).first_or_404()

    if action == 'fav':
        current_user.like_group(group)
        db.session.commit()

    if action == 'unfav':
        current_user.unlike_group(group)
        db.session.commit()

    return redirect(request.referrer)

# Route for deleting a group
@groups.route('/delete/<int:group_id>/')
@login_required
@confirmed_required
def delete_group(group_id):

    group = Group.query.filter_by(id=group_id).first_or_404()

    if group.author == current_user.username:
        db.session.delete(group)
        db.session.commit()

        flash(f'Your group with ID {group.course_id} was successfully deleted.', 'info')
        return redirect(request.referrer)

    else:
        flash("You don't own this group, therefore you can not delete it.", 'alert')
        return redirect(request.referrer)