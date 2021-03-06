import re, calendar, datetime, time, pytz


def get_key_filtered_dict(x, matcher=lambda key: True):
	return {k: v for k, v in x.__dict__.items() if matcher(k)}


def get_key_filtered_properties(obj, matcher=lambda key: True):
	assert not isinstance(obj, type), "must be object, not class"
	def _fix(v):
		v = v.fget(obj)
		return v if not callable(v) else v()
	d = get_key_filtered_dict(type(obj), matcher)
	return {k: _fix(v) for k, v in d.items() if isinstance(v, property)}


def get_full_dict(obj, matcher=lambda key: True):
	d = get_key_filtered_dict(obj, matcher)
	if not isinstance(obj, type):
		cd = get_key_filtered_properties(obj, matcher)
		d.update(cd)
	return d


def dict_safe_transform(d, transformer=lambda val: val):
	def _transformer(val):
		try: return transformer(val)
		except: return val
	return {k: _transformer(v) for k, v in d.items()}


class dictable:

	def __init__(self, keypattern="", transformer=None):
		self.matcher = re.compile(keypattern)
		self.transformer = transformer or (lambda val: val)

	def __call__(self, cls):
		def _to_dict(obj):
			d = get_full_dict(obj, self.matcher.match)
			d = dict_safe_transform(d, self.transformer)
			return d

		setattr(cls, "to_dict", _to_dict)
		return cls


class printable:

	def __init__(self, keypattern="[^_].*", transformer=None):
		self.matcher = re.compile(keypattern)
		self.transformer = transformer or (lambda val: val)

	def __call__(self, cls):
		def _str(obj):
			d = get_full_dict(obj, self.matcher.match)
			d = dict_safe_transform(d, self.transformer)
			return "%s%s" % (cls.__name__, d)

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


def utc(s, format="%Y-%m-%d %H:%M:%S"):
	return datetime.datetime.fromtimestamp(calendar.timegm(time.strptime(s, format)[0:6]))


def utcnow():
	return datetime.datetime.fromtimestamp(time.time()).replace(tzinfo=pytz.timezone("UTC"))


def add_mock_records(db):
	from sqlalchemy import exc
	from application.routes.leads.models import Lead
	from application.routes.touches.models import Touch

	print("***** ADDING MOCK RECORDS *****")

	leads = (
		{"name": "Dejan Budimir", "company": "n/a", "phone": "0123456789", "email": "Dejan@Budimir.de"},
		{"name": "Dejan Budimir", "company": "n/a", "phone": "0123456789", "email": "Dejan@Budimir.com"},
	)

	touches = (
		{"date": utc("2020-03-20 10:00:00"), "description": "...", "lead_id": 1},
		{"date": utc("2020-03-20 10:00:01"), "description": "...", "lead_id": 1},
		{"date": utc("2020-03-20 10:00:02"), "description": "...", "lead_id": 2},
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
