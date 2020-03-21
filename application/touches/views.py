from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy import exc

from application import db

from application.leads.models import Lead
from application.touches.models import Touch
from application.touches.forms import AddTouchForm


touches = Blueprint("touches", __name__)


@touches.route("/")
def index():
	dates_order = request.args.get("dates_order", "ascending")
	return render_template("touches_index.html", touches=Touch.query.all(), dates_order=dates_order)


@touches.route("/lead/<lead_id>")
def for_lead(lead_id):
	dates_order = request.args.get("dates_order", "ascending")
	lead = Lead.query.get_or_404(lead_id)
	return render_template("touches_for_lead.html", lead=lead, touches=lead.touches, dates_order=dates_order)


@touches.route("/add")
def add():
	return render_template("touches_add.html")


@touches.route("/add/lead/<id>", methods=['GET', 'POST'])
def add_for_lead(id):
	lead = Lead.query.get_or_404(id)
	form = AddTouchForm()

	if form.validate_on_submit():

		print(form)
		item = Touch(lead_id=id, **form.to_dict())

		try:
			db.session.add(item)
			db.session.commit()
		except exc.IntegrityError as e:
			flash("Please wait a second and try again.")
			print(e)
			db.session.rollback()
		except exc.SQLAlchemyError as e:
			flash("An unknown error occurred while adding Touch.")
			print(e)
			db.session.rollback()
		else:
			return redirect(url_for("touches.for_lead", lead_id=id))

	return render_template("touches_add_for_lead.html", form=form, lead=lead)
