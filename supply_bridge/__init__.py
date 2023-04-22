from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
# from flask_principal import Principal
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_jsglue import JSGlue
from flask_admin import Admin
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
jsglue = JSGlue(app)


from supply_bridge import routes, models
from flask_admin.contrib.sqla import ModelView
# Flask and Flask-SQLAlchemy initialization here
admin = Admin(app)
class _Admin(Admin):
    def add_model_view(self, model):
        self.add_view(ModelView(model, db.session))

    def add_model_views(self, models):
        for model in models:
            self.add_model_view(model)


model_dict = {x[0]: x[1] for x in db.metadata.tables.items()}
model_list = [d for d in model_dict.values()]
# admin.add_model_views(model_list)
# print(model_list)

# class CustomModelView(ModelView):
#     def __init__(self, model, session, **kwargs):
#         super(CustomModelView, self).__init__(model, session, **kwargs)

#     def get_list(self, *args, **kwargs):
#         # Get all models
#         models = [cls for cls in db.Model._decl_class_registry.values() if isinstance(cls, type) and issubclass(cls, db.Model)]
#         # Add them to the view
#         for model in models:
#             self._add_model(model)
#         return super(CustomModelView, self).get_list(*args, **kwargs)

# # Register the view
# admin.add_view(CustomModelView(db.Model, db.session))
# admin.add_view(ModelView(models.User, db.session))
# admin.add_view(ModelView(Post, db.session))
# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
security = Security(app, user_datastore)
