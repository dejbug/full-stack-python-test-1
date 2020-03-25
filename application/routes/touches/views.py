from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from sqlalchemy import exc

from application import db, utils

from application.routes.leads.models import Lead
from application.routes.touches.models import Touch
from application.routes.touches.forms import AddTouchForm, AddTouchForm2


touches = Blueprint("touches", __name__)


@touches.route("/")
def index():

	if utils.update_session_from_request():
		return redirect(url_for("touches.index"))

	return render_template("touches_index.html", touches=Touch.query.all(), dates_order=session["dates_order"], dates_tz=session["dates_tz"])


@touches.route("/lead/<lead_id>")
def for_lead(lead_id):

	if utils.update_session_from_request():
		return redirect(url_for("touches.for_lead", lead_id=lead_id))

	lead = Lead.query.get_or_404(lead_id)

	return render_template("touches_for_lead.html", lead=lead, touches=lead.touches, dates_order=session["dates_order"], dates_tz=session["dates_tz"])


@touches.route("/add", methods=["GET", "POST"])
def add():
	form = AddTouchForm2()

	if form.validate_on_submit():

		print(form)

		lead_id = form.extract_lead_id()
		if lead_id:

			item = Touch(**form.to_dict())

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
				return redirect(url_for("touches.index"))

	return render_template("touches_add.html", form=form)


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
