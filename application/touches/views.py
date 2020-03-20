from flask import Blueprint, render_template, url_for

import application.touches.models as models


touches = Blueprint("touches", __name__)


@touches.route("/")
def index():
	return render_template("touches_index.html", touches=models.Touch.query.all())


@touches.route("/add")
def add():
	return render_template("touches_add.html")
