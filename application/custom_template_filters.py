from traceback import print_exc

from application import app


class Error(Exception): pass


@app.template_filter()
def length(obj):

	try: return obj.count()
	except: print_exc()

	try: return len(obj)
	except: print_exc()

	raise Error("unable to determine length of object")


@app.template_filter()
def dateform(obj, format="%Y-%m-%d / %H-%M-%S"):

	try: return obj.strftime(format)
	except: print_exc()
