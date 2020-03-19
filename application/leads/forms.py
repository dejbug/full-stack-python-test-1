from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

from application import utils


@utils.dictable("name|company|phone|email", lambda val: val.data)
@utils.printable("name|company|phone|email", lambda val: val.data)
class AddLeadForm(FlaskForm):

	name = StringField("Name", validators=[DataRequired()])
	company = StringField("Company", validators=[DataRequired()])
	phone = StringField("Phone", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])

	submit = SubmitField("Add")
