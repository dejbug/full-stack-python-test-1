from application import db, utils


@utils.printable()
class Lead(db.Model):

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String)
	company = db.Column(db.String)
	phone = db.Column(db.String)
	email = db.Column(db.String, unique=True)
