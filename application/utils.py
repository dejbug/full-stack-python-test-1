import re


class dictable:
	def __init__(self, keypattern="", transformer=None):
		self.matcher = re.compile(keypattern)
		self.transformer = transformer or (lambda val: val)

	def __call__(self, cls):
		def _to_dict(obj):
			return {key: self.transformer(val) for key, val in obj.__dict__.items() if self.matcher.match(key)}
		setattr(cls, "to_dict", _to_dict)
		return cls


class printable:
	def __init__(self, keypattern="[^_].*", transformer=None):
		self.matcher = re.compile(keypattern)
		self.transformer = transformer or (lambda val: val)

	def __call__(self, cls):
		def _str(obj):
			return "%s%s" % (cls.__name__, {key: self.transformer(val) for key, val in obj.__dict__.items() if self.matcher.match(key)})
		setattr(cls, "__str__", _str)
		return cls


def create_secret_key(length=32):
	from os import urandom
	from base64 import b64encode
	return b64encode(urandom(length), b"#!").decode("ansi")


def create_secret_key_file(path, length=32):
	from os.path import exists, getsize
	if not exists(path) or getsize(path) < length:
		with open(path, "w") as file:
			file.write(create_secret_key(length))


def init_session():
	from flask import session
	if not "dates_order" in session: session["dates_order"] = None
	if not "dates_tz" in session: session["dates_tz"] = None


def update_session_from_request():
	from flask import session, request

	dates_order = request.args.get("dates_order")
	dates_tz = request.args.get("dates_tz")

	need_redirect = False

	if dates_order:
		session["dates_order"] = dates_order
		need_redirect = True

	if dates_tz:
		session["dates_tz"] = dates_tz
		need_redirect = True

	return need_redirect


def add_mock_records(db):
	import datetime
	from sqlalchemy import exc
	from application.routes.leads.models import Lead
	from application.routes.touches.models import Touch

	print("***** ADDING MOCK RECORDS *****")

	dt_format = "%Y-%m-%d %H:%M:%S %Z"
	dt = lambda s: datetime.datetime.strptime(s, dt_format)

	leads = (
		{"name": "Dejan Budimir", "company": "n/a", "phone": "0123456789", "email": "Dejan@Budimir.de"},
		{"name": "Dejan Budimir", "company": "n/a", "phone": "0123456789", "email": "Dejan@Budimir.com"},
	)

	touches = (
		{"date": dt("2020-03-20 10:00:00 UTC"), "description": "...", "lead_id": 1},
		{"date": dt("2020-03-20 10:00:01 UTC"), "description": "...", "lead_id": 1},
		{"date": dt("2020-03-20 10:00:02 UTC"), "description": "...", "lead_id": 2},
	)

	for kwargs in leads:
		db.session.rollback()
		db.session.add(Lead(**kwargs))
		try: db.session.commit()
		except exc.IntegrityError: pass
		except exc.SQLAlchemyError as e: print(e)

	for kwargs in touches:
		db.session.rollback()
		db.session.add(Touch(**kwargs))
		try: db.session.commit()
		except exc.IntegrityError: pass
		except exc.SQLAlchemyError as e: print(e)
