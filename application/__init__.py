SECRET_KEY_FILE_PATH = "key.secret"
DATABASE_PATH = "sqlite:///../application.db"

from application.utils import create_secret_key_file
create_secret_key_file(SECRET_KEY_FILE_PATH)

from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = open(SECRET_KEY_FILE_PATH).read()

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
db = SQLAlchemy(app)

from application.routes.views import index

from application.routes.leads.views import leads
from application.routes.touches.views import touches
app.register_blueprint(leads, url_prefix="/leads")
app.register_blueprint(touches, url_prefix="/touches")

from application.custom_template_filters import *
