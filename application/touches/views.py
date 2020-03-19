from flask import Blueprint, render_template, url_for


touches = Blueprint("touches", __name__)

@touches.route("/")
def index():
	return render_template("touches_index.html")

@touches.route("/add")
def add():
	return render_template("touches_add.html")
