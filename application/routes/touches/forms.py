import re

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email

from application import utils


@utils.dictable("description", lambda val: val.data)
@utils.printable("description", lambda val: val.data)
class AddTouchForm(FlaskForm):

	description = StringField("Description", validators=[DataRequired()])

	submit = SubmitField("Add")


@utils.dictable("lead_id|description", lambda val: val.data)
@utils.printable("lead_id|description", lambda val: val.data)
class AddTouchForm2(FlaskForm):

	lead_query = StringField("Lead", validators=[DataRequired()])
	description = StringField("Description", validators=[DataRequired()])

	submit = SubmitField("Add")

	@property
	def lead_id(self):
		return self.extract_lead_id()

	def extract_lead_id(self):
		x = re.search(r'^#(\d+)', self.lead_query.data)
		if x: return int(x.group(1))
