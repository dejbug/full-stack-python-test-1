SECRET_KEY_FILE_PATH = "key.secret"

from application.utils import create_secret_key_file
create_secret_key_file(SECRET_KEY_FILE_PATH)

from flask import Flask
app = Flask(__name__, template_folder="_templates", static_folder="_static")
app.config["SECRET_KEY"] = open(SECRET_KEY_FILE_PATH).read()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../application.db"
db = SQLAlchemy(app)

from application.views import index

from application.leads.views import leads
from application.touches.views import touches
app.register_blueprint(leads, url_prefix="/leads")
app.register_blueprint(touches, url_prefix="/touches")

from application.custom_template_filters import *
