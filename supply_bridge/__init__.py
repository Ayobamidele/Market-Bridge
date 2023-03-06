from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
# from flask_principal import Principal
from .config import Config
app = Flask(__name__,template_folder='templates') 
app.config.from_object(Config)




db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
mail = Mail(app)
# principals = Principal(app)
login = LoginManager(app)
login.login_view = 'login'
  



from supply_bridge import routes, models
