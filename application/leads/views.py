from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddLeadForm(FlaskForm):

	name = StringField("Name", validators=[DataRequired()])
	company = StringField("Company", validators=[DataRequired()])
	phone = StringField("Phone", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])

	submit = SubmitField("Add")


leads = Blueprint("leads", __name__, template_folder="_templates", static_folder="_static")


@leads.route("/")
def index():
	return render_template("index.html")


@leads.route("/add", methods=['GET', 'POST'])
def add():
	form = AddLeadForm()
	print("hi")
	if form.validate_on_submit():
		print("ho")
		return redirect(url_for("leads.index"))
	return render_template("add.html", form=form)
