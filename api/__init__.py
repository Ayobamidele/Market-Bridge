from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_security import Security, SQLAlchemySessionUserDatastore
from api.db import db, init_app, get_db
from api.v1.models import User, Role
from pages import pages

# Initialize extensions
migrate = Migrate()
bootstrap = Bootstrap5()
mail = Mail()
login = LoginManager()
login.login_view = 'login'

def create_app(config_class='api.utils.config.Config'):
    app = Flask(__name__, template_folder='../api/v1/templates')
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)  # Initialize db
    migrate.init_app(app, db, render_as_batch=True, compare_type=True)
    bootstrap.init_app(app)
    mail.init_app(app)
    login.init_app(app)

    # Register Blueprints
    from api.v1.routes import v1
    app.register_blueprint(v1)
    app.register_blueprint(pages)

    # Initialize the database with the app
    init_app(app)  # Register the close_db function with Flask

    # Security Setup
    # Make sure we are within the app context when initializing SQLAlchemySessionUserDatastore
    with app.app_context():  # Ensure app context is pushed
        user_datastore = SQLAlchemySessionUserDatastore(get_db(), User, Role)
        security = Security(app, user_datastore)

    # Shell context processor
    @app.shell_context_processor
    def make_shell_context():
        return {x[0]: x[1] for x in db.metadata.tables.items()}

    return app
