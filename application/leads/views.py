from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import exc

from application import db

import application.leads.forms as forms
import application.leads.models as models


leads = Blueprint("leads", __name__)


@leads.route("/")
def index():
	return render_template("leads_index.html", leads=models.Lead.query.all())


@leads.route("/add", methods=['GET', 'POST'])
def add():
	form = forms.AddLeadForm()

	if form.validate_on_submit():

		print(form)
		lead = models.Lead(**form.to_dict())

		db.session.add(lead)
		try:
			db.session.commit()
		except exc.IntegrityError as e:
			flash("Lead already exists.")
			print(e)
		except exc.SQLAlchemyError as e:
			flash("An unknown error occurred while adding Lead.")
			print(e)

		return redirect("leads_index.html")

	elif form.errors:
		flash(form.errors)

	return render_template("leads_add.html", form=form)
