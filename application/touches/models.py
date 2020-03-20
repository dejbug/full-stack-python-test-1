import datetime

from application import db, utils


@utils.printable()
class Touch(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	date = db.Column(db.DateTime, unique=True, default=datetime.datetime.utcnow)
	
	description = db.Column(db.String)

	lead_id = db.Column(db.Integer, db.ForeignKey("lead.id"))

	lead = db.relationship("Lead", backref=db.backref("touch", lazy="dynamic"))
