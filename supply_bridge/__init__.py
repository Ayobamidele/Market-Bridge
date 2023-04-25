from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
# from flask_principal import Principal
from flask_statistics import Statistics
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_jsglue import JSGlue
from flask_admin import Admin
from .config import Config
from flask_serialize import FlaskSerialize
from flask_marshmallow import Marshmallow



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
fs_mixin = FlaskSerialize(db)
ma = Marshmallow(app)


# class _Admin(Admin):
#     def add_model_view(self, model):
#         self.add_view(ModelView(model, db.session))

#     def add_model_views(self, models):
#         for model in models:
#             self.add_model_view(model)


# def result():
# 	classes, models, table_names = [], [], []
# 	for clazz in db.Model.registry._class_registry.values():
# 		try:
# 			table_names.append(clazz.__tablename__)
# 			classes.append(clazz)
# 		except:
# 			pass
# 	for table in db.metadata.tables.items():
# 		if table[0] in table_names:
# 			models.append(classes[table_names.index(table[0])])
# 	return models

# admin = _Admin(app)

from supply_bridge import routes, models
from flask_admin.contrib.sqla import ModelView
# for i in result():
# 	admin.add_model_view(i)


statistics = Statistics(app, db, models.Request)
print(statistics.api)
# Flask and Flask-SQLAlchemy initialization here
# admin.add_model_views(model_list)
# print(model_list)

# admin.add_view(ModelView(models.User, db.session))
# admin.add_view(ModelView(Post, db.session))
# load users, roles for a session
user_datastore = SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
security = Security(app, user_datastore)
