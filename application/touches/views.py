from flask import Blueprint, render_template, url_for

from application.leads.models import Lead
from application.touches.models import Touch


touches = Blueprint("touches", __name__)


@touches.route("/")
def index():
	return render_template("touches_index.html", touches=Touch.query.all())


@touches.route("/lead/<id>")
def by_lead_id(id):
	s = ""
	lead = Lead.query.get_or_404(id)
	return render_template("touches_by_lead_id.html", lead=lead, touches=lead.touches)
	return s


@touches.route("/add")
def add():
	return render_template("touches_add.html")


@touches.route("/add/lead/<id>")
def add_for_lead(id):
	return "Add (for Lead)"
