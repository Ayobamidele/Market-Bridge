from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
# from flask_principal import Principal
from flask_security import Security, SQLAlchemySessionUserDatastore

from .config import Config

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True, compare_type=True)
bootstrap = Bootstrap5(app)
mail = Mail(app)
# principals = Principal(app)
login = LoginManager(app)
login.login_view = 'login'

from supply_bridge import routes, models

# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
security = Security(app, user_datastore)
