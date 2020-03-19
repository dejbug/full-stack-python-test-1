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
