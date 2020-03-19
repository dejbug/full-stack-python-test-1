
def stringify(cls):
	def _str(obj):
		return "Touch%s" % {key: val for key, val in obj.__dict__.items() if not key.startswith("_")}
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
