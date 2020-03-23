from application import db, utils


@utils.printable()
class Touch(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	date = db.Column(db.DateTime(True), unique=True, default=utils.utcnow)

	description = db.Column(db.String)

	lead_id = db.Column(db.Integer, db.ForeignKey("lead.id"))

	lead = db.relationship("Lead", backref=db.backref("touches", lazy="dynamic"))
