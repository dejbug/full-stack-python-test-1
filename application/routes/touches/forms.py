from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email

from application import utils


@utils.dictable("description", lambda val: val.data)
@utils.printable("description", lambda val: val.data)
class AddTouchForm(FlaskForm):

	description = StringField("Description", validators=[DataRequired()])

	submit = SubmitField("Add")
