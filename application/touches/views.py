from flask import Blueprint, render_template

touches = Blueprint("touches", __name__, template_folder="_templates")

@touches.route("/")
def index():
	return render_template("index.html")

@touches.route("/add")
def add():
	return render_template("add.html")
