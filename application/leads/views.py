from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import exc

from application import db

from application.leads.models import Lead
from application.leads.forms import AddLeadForm


leads = Blueprint("leads", __name__)


@leads.route("/")
def index():
	return render_template("leads_index.html", leads=Lead.query.all())


@leads.route("/<id>")
def by_id(id):
	lead = Lead.query.get_or_404(id)
	return str(lead)


@leads.route("/add", methods=['GET', 'POST'])
def add():
	form = AddLeadForm()

	if form.validate_on_submit():

		print(form)
		item = Lead(**form.to_dict())

		db.session.add(item)
		try:
			db.session.commit()
		except exc.IntegrityError as e:
			flash("Lead already exists for this email.")
			print(e)
		except exc.SQLAlchemyError as e:
			flash("An unknown error occurred while adding Lead.")
			print(e)
		else:
			return redirect(url_for("leads.index"))

	elif form.errors:
		flash(form.errors)

	return render_template("leads_add.html", form=form)
