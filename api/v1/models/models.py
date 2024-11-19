# from datetime import datetime
# from sqlalchemy_utils import PhoneNumber
# from api import db, login
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# from time import time
# import json
# from api.v1.models import CRUDMixin
# from api.utils.config import config

# # mapping tables
# UserGroup = db.Table(
#     'user_group', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
# )


# UserRole = db.Table(
#     'user_role', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
# )

# UserOrder = db.Table(
#     'user_order', db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'),)
# )


# OrderItems = db.Table(
#     'order_items', db.Model.metadata,
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
#     db.Column('orderitem_id', db.Integer, db.ForeignKey('orderitem.id')),
# )

# OrderSuppliers = db.Table(
#     'order_suppliers', db.Model.metadata,
#     db.Column('supplier_id', db.Integer, db.ForeignKey('suppliers.id')),
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'),)
# )

# OrderVendors = db.Table(
#     'order_vendors', db.Model.metadata,
#     db.Column('vendor_id', db.Integer, db.ForeignKey('vendor.id')),
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'),)
# )

# OrderItemsVendor = db.Table(
#     'order_items_vendor', db.Model.metadata,
#     db.Column('vendor_id', db.Integer, db.ForeignKey('vendor.id')),
#     db.Column('orderitem_id', db.Integer, db.ForeignKey('orderitem.id')),
# )

# class User(db.Model, CRUDMixin,  UserMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(20), nullable=False)
#     lastname = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     # Phone number
#     _phone_number = db.Column(db.Unicode(255), nullable=False)
#     phone_country_code = db.Column(db.Unicode(8))
#     phone_number = db.orm.composite(
#         PhoneNumber,
#         _phone_number,
#         phone_country_code
#     )

#     roles = db.relationship('Role', secondary=UserRole)
#     groups = db.relationship('Group', secondary=UserGroup)

#     image_file = db.Column(db.String(20), nullable=False,default='\static\images\default.jpg')
#     password = db.Column(db.String(20), nullable=False)
#     date_created = db.Column(
#         db.DateTime, nullable=False, default=datetime.utcnow)
#     orders = db.relationship('Order', secondary=UserOrder,back_populates="contributors",uselist=True)
#     is_active = db.Column(db.Boolean)
#     notifications = db.relationship('Notification', backref='reciever', lazy='dynamic')


#     def __repr__(self):
#         return f"User('{self.firstname}', '{self.lastname}','{self.phone_number}' ,'{self.email}','{self.image_file}')"

#     def is_active(self):
#         return self.active
    
#     def is_admin(self):
#         return "Admin" in [role.name for role in self.roles]

#     def set_authenticated(self, value):
#         if value:
#             self._authenticated = True

#     def is_authenticated(self):
#         return self._authenticated

#     def set_password(self, secret):
#         self.password = generate_password_hash(secret)

#     def check_password(self, secret):
#         return check_password_hash(self.password, secret)

#     def get_reset_password_token(self, expires_in=600):
#         return jwt.encode(
#             {'reset_password': self.id, 'exp': time() + expires_in},
#             config.SECRET_KEY, algorithm='HS256')

#     @staticmethod
#     def verify_reset_password_token(token):
#         try:
#             id = jwt.decode(token, config.SECRET_KEY,
#                             algorithms=['HS256'])['reset_password']
#         except:
#             return
#         return User.query.get(id)

#     def unread_notifications(self):
#         return self.notifications.filter_by(read=False).all()
    
# class Notification(db.Model, CRUDMixin):
#     __tablename__ = 'notifications'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     timestamp = db.Column(db.Float, default=time)
#     payload_json = db.Column(db.Text)
#     read = db.Column(db.Boolean,default=False)

#     def get_data(self):
#         return json.loads(str(self.payload_json))


# @login.user_loader
# def load_user(user):
#     print(User.query.get(int(user)))
#     return User.query.get(int(user))

# # @login.request_loader
# # def request_loader(request):
# #     # first, try to login using the api_key url arg
# #     api_key = request.args.get('api_key')
# #     print(dir(request), request.json())
# #     if api_key:
# #         user = User.query.filter_by(api_key=api_key).first()
# #         if user:
# #             return user

# #     # next, try to login using Basic Auth
# #     api_key = request.headers.get('Authorization')
# #     if api_key:
# #         api_key = api_key.replace('Basic ', '', 1)
# #         try:
# #             api_key = base64.b64decode(api_key)
# #         except TypeError:
# #             pass
# #         user = User.query.filter_by(api_key=api_key).first()
# #         if user:
# #             return user

# #     # finally, return None if both methods did not login the user
# #     return None


# class Group(db.Model):
#     __tablename__ = 'groups'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)

#     def __repr__(self):
#         return self.name


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)

#     def __repr__(self):
#         return self.name


# class Vendor(db.Model, CRUDMixin):
#     __tablename__ = "vendor"

#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(20), unique=True, nullable=False)
#     lastname = db.Column(db.String(20), unique=True, nullable=False)
#     description = db.Column(db.String(1000), nullable=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     date_created = db.Column(
#         db.DateTime, nullable=False, default=datetime.utcnow)
#     _phone_number = db.Column(db.Unicode(255), nullable=False)
#     phone_country_code = db.Column(db.Unicode(8))
#     phone_number = db.orm.composite(
#         PhoneNumber,
#         _phone_number,
#         phone_country_code
#     )
#     orders = db.relationship('Order', secondary=OrderVendors, back_populates="vendors",uselist=True)
#     order_items = db.relationship('OrderItem', secondary=OrderItemsVendor, back_populates="vendors",uselist=True)
    

# class Supplier(db.Model, CRUDMixin):
#     __tablename__ = 'suppliers'

#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(20), unique=True, nullable=False)
#     lastname = db.Column(db.String(20), unique=True, nullable=False)
#     description = db.Column(db.String(1000), nullable=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     date_created = db.Column(
#         db.DateTime, nullable=False, default=datetime.utcnow)
#     _phone_number = db.Column(db.Unicode(255), nullable=False)
#     phone_country_code = db.Column(db.Unicode(8))
#     phone_number = db.orm.composite(
#         PhoneNumber,
#         _phone_number,
#         phone_country_code
#     )
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     orders = db.relationship('Order', secondary=OrderSuppliers,back_populates="suppliers",uselist=True)



# class Order(db.Model, CRUDMixin):
#     __tablename__ = "order"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_created = db.Column(
#         db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     # owner = db.relationship('User', secondary=UserOrder, backref=db.backref('user', lazy='dynamic'), back_populates="orders")
#     contributors = db.relationship('User', secondary=UserOrder, back_populates="orders",uselist=True)
#     suppliers = db.relationship('Supplier', secondary=OrderSuppliers, back_populates="orders",uselist=True)
#     vendors = db.relationship('Vendor', secondary=OrderVendors, back_populates="orders",uselist=True)
#     order_items = db.relationship('OrderItem', secondary=OrderItems, back_populates="orders",uselist=True)

#     def __repr__(self):
#         return f"Order('{self.title}','{self.date_created}')"


# class OrderItem(db.Model, CRUDMixin):
#     __tablename__ = "orderitem"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.DECIMAL)
#     vendors = db.relationship('Vendor', secondary=OrderItemsVendor, back_populates="order_items",uselist=True)
#     orders = db.relationship('Order', secondary=OrderItems,back_populates="order_items",uselist=True)

