from flask import session, redirect, url_for
from application import app, utils


@app.route("/")
def index():
	utils.init_session()
	return redirect(url_for("leads.index"))
