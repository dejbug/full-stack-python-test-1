from traceback import print_exc

from pytz import timezone

from application import app


class Error(Exception): pass


@app.template_filter()
def length(obj):

	if hasattr(obj, "__len__"):
		return len(obj)

	try: return obj.count()
	except: print_exc()

	raise Error("unable to determine length of object")


@app.template_filter()
def datezone(obj, tz="UTC"):

	if not tz or tz == "local":
		tz = app.config["LOCAL_TIMEZONE"]

	try: return obj.astimezone(timezone(tz))
	except: print_exc()

	return obj


@app.template_filter()
def dateform(obj, format="%Y-%m-%d - %H:%M:%S"):

	try: return obj.strftime(format)
	except: print_exc()

	return obj


@app.template_filter()
def date_ordered(obj, dates_order=None):

	reverse = dates_order == "descending"

	try: return sorted(obj, key=lambda it: it.date, reverse=reverse)
	except: print_exc()

	return obj
