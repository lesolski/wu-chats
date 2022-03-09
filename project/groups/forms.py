# project/groups/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, InputRequired

class AddGroupForm(FlaskForm):
	semester = SelectField('Semester', choices=[('SS21', 'SS21'), ('WS21', 'WS21')], validators=[InputRequired(), DataRequired()])
	group_name = StringField('Group Name', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "Group Name"})
	course_id = IntegerField('Course ID', validators=[InputRequired(message="Course ID must be a 4 digits number"), DataRequired(message="Course ID must be a 4 digits number")], render_kw={"placeholder": "Course ID"})
	professors = StringField('Lecturer', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "Lecturer"})
	platform = SelectField('Platform', choices=[('WhatsApp', 'WhatsApp'), ('Telegram', 'Telegram')], validators=[InputRequired(), DataRequired()])
	grouplink = StringField('Group Link', validators=[InputRequired(), DataRequired()], render_kw={"placeholder": "Invite Link to the group"})
	show_admin = RadioField('Visibility', coerce=int, choices=[(1, 'Show my email as admin'), (0, 'Post anonymously')], validators=[InputRequired()])
	submit = SubmitField('Submit')


	def validate_grouplink(self, field):

		if self.platform.data == 'WhatsApp' and field.data[:26] != 'https://chat.whatsapp.com/':
			raise ValidationError('Since you choose WhatsApp, you can only publish WhatsApp link for this group.')

		elif self.platform.data == 'Telegram' and field.data[:22] != 'https://t.me/joinchat/':
			raise ValidationError('Since you choose Telegram, you can only publish Telegram link for this group.')

	def validate_course_id(self, field):
		if len(str(field.data)) != 4:
			raise ValidationError('Course ID must be a 4 digits number.')

class SearchForm(FlaskForm):
	search = IntegerField('Search', render_kw={"placeholder": "Search here with course name or course ID"})
