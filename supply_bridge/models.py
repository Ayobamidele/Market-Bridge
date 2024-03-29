from datetime import datetime
from sqlalchemy_utils import PhoneNumber
from supply_bridge import db, login, Config, fs_mixin, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
import json
from supply_bridge.utility import CRUDMixin
import enum
from random_username.generate import generate_username
from decimal import Decimal 
from sqlalchemy.types import TypeDecorator, Integer
from marshmallow import fields



class SqliteDecimal(TypeDecorator):
	# This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
	# from Python to Integers which is later stored in Sqlite database.
	impl = Integer

	def __init__(self, scale):
		# It takes a 'scale' parameter, which specifies the number of digits
		# to the right of the decimal point of the number in the column.
		TypeDecorator.__init__(self)
		self.scale = scale
		self.multiplier_int = 10 ** self.scale

	def process_bind_param(self, value, dialect):
		# e.g. value = Column(SqliteDecimal(2)) means a value such as
		# Decimal('12.34') will be converted to 1234 in Sqlite
		if value is not None:
			value = int(Decimal(value) * self.multiplier_int)
		return value

	def process_result_value(self, value, dialect):
		# e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
		# when query takes place.
		if value is not None:
			value = Decimal(value) / self.multiplier_int
		return value


class OrderStatus(enum.Enum):
	planning = "planning"
	shopping = "shopping"
	delivered_unpaid = "waiting payment"
	delivered_paid = "delivered"

class MeasurementType(enum.Enum):
	price = "Price"
	measure = "Measure"

	def __str__(self):
		return self.value

class InvitationStatus(enum.Enum):
	accepted = "Accepted"
	denied = "Denied"
	pending = "Pending"

class OrderGroupRoleStatus(enum.Enum):
	admin = "Admin"
	moderator = "Moderator"
	contributor = "Contributor"

# mapping tables
UserGroup = db.Table(
	"user_group",
	db.Model.metadata,
	db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
	db.Column("group_id", db.Integer, db.ForeignKey("groups.id")),
)


UserRole = db.Table(
	"user_role",
	db.Model.metadata,
	db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
	db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)

UserOrder = db.Table(
	"user_order",
	db.Model.metadata,
	db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
	db.Column(
		"order_id",
		db.Integer,
		db.ForeignKey("order.id"),
	),
)


OrderItems = db.Table(
	"order_items",
	db.Model.metadata,
	db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
	db.Column("orderitem_id", db.Integer, db.ForeignKey("orderitem.id")),
)

OrderSuppliers = db.Table(
	"order_suppliers",
	db.Model.metadata,
	db.Column("supplier_id", db.Integer, db.ForeignKey("suppliers.id")),
	db.Column(
		"order_id",
		db.Integer,
		db.ForeignKey("order.id"),
	),
)

OrderGroups = db.Table(
	"order_groups",
	db.Model.metadata,
	db.Column("ordergroup_id", db.Integer, db.ForeignKey("ordergroup.id")),
	db.Column(
		"order_id",
		db.Integer,
		db.ForeignKey("order.id"),
	),
)

OrderGroupMembers = db.Table(
	"order_group_members",
	db.Model.metadata,
	db.Column("ordergrouprole", db.Integer, db.ForeignKey("ordergrouprole.id")),
	db.Column(
		"ordergroup_id",
		db.Integer,
		db.ForeignKey("ordergroup.id"),
	),
)

OrderVendors = db.Table(
	"order_vendors",
	db.Model.metadata,
	db.Column("vendor_id", db.Integer, db.ForeignKey("vendor.id")),
	db.Column(
		"order_id",
		db.Integer,
		db.ForeignKey("order.id"),
	),
)

OrderItemsVendor = db.Table(
	"order_items_vendor",
	db.Model.metadata,
	db.Column("vendor_id", db.Integer, db.ForeignKey("vendor.id")),
	db.Column("orderitem_id", db.Integer, db.ForeignKey("orderitem.id")),
)


class User(db.Model, CRUDMixin, UserMixin):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	# Phone number
	_phone_number = db.Column(db.Unicode(255), nullable=False)
	phone_country_code = db.Column(db.Unicode(8))
	phone_number = db.orm.composite(PhoneNumber, _phone_number, phone_country_code)

	roles = db.relationship("Role", secondary=UserRole)
	groups = db.relationship("Group", secondary=UserGroup)

	image_file = db.Column(
		db.String(20), nullable=False, default="\static\images\default.jpg"
	)
	password = db.Column(db.String(20), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	orders = db.relationship(
		"Order", secondary=UserOrder, back_populates="contributors", uselist=True
	)
	is_active = db.Column(db.Boolean)
	notifications = db.relationship("Notification", backref="reciever", lazy="dynamic")

	def __repr__(self):
		return f"User('{self.firstname}', '{self.lastname}','{self.phone_number}' ,'{self.email}','{self.image_file}')"

	def is_active(self):
		return self.active

	def is_admin(self):
		return "Admin" in [role.name for role in self.roles]

	def set_authenticated(self, value):
		if value:
			self._authenticated = True

	def is_authenticated(self):
		return self._authenticated

	def set_password(self, secret):
		self.password = generate_password_hash(secret)

	def check_password(self, secret):
		return check_password_hash(self.password, secret)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{"reset_password": self.id, "exp": time() + expires_in},
			Config.SECRET_KEY,
			algorithm="HS256",
		)

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])[
				"reset_password"
			]
		except:
			return
		return User.query.get(id)

	def unread_notifications(self):
		return self.notifications.filter_by(read=False).all()

	def set_username(self, username=None):
		if username:
			self.username = username
		self.username = generate_username(1)[0]

	def order_exist(self, id=None,title=None):
		if id:
			return id in [i.id for i in self.orders]
		return title in [i.title for i in self.orders]
	

class Notification(db.Model, CRUDMixin):
	__tablename__ = "notifications"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	timestamp = db.Column(db.Float, default=time)
	payload_json = db.Column(db.Text)
	read = db.Column(db.Boolean, default=False)

	def get_data(self):
		return json.loads(str(self.payload_json))





class Invitation(db.Model, CRUDMixin):
	__tablename__ = "invitation"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	group_id = db.Column(db.Integer, db.ForeignKey("ordergroup.id"))
	timestamp = db.Column(db.Float, default=time)
	payload_json = db.Column(db.Text)
	read = db.Column(db.Boolean, default=False)
	status = db.Column(
		db.Enum(InvitationStatus),
		default=InvitationStatus.pending,
		# nullable=False
	)

	def get_data(self):
		return json.loads(str(self.payload_json))


@login.user_loader
def load_user(user):
	return User.query.get(int(user))


# @login.request_loader
# def request_loader(request):
#     # first, try to login using the api_key url arg
#     api_key = request.args.get('api_key')
#     print(dir(request), request.json())
#     if api_key:
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user

#     # next, try to login using Basic Auth
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user

#     # finally, return None if both methods did not login the user
#     return None


class Group(db.Model, CRUDMixin):
	__tablename__ = "groups"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False, unique=True)

	def __repr__(self):
		return self.name


class Role(db.Model, CRUDMixin):
	__tablename__ = "roles"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False, unique=True)

	def __repr__(self):
		return self.name


class Vendor(db.Model, CRUDMixin):
	__tablename__ = "vendor"

	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), unique=True, nullable=False)
	lastname = db.Column(db.String(20), unique=True, nullable=False)
	description = db.Column(db.String(1000), nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	_phone_number = db.Column(db.Unicode(255), nullable=False)
	phone_country_code = db.Column(db.Unicode(8))
	phone_number = db.orm.composite(PhoneNumber, _phone_number, phone_country_code)
	orders = db.relationship(
		"Order", secondary=OrderVendors, back_populates="vendors", uselist=True
	)
	order_items = db.relationship(
		"OrderItem", secondary=OrderItemsVendor, back_populates="vendors", uselist=True
	)


class Supplier(db.Model, CRUDMixin):
	__tablename__ = "suppliers"

	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(20), unique=True, nullable=False)
	lastname = db.Column(db.String(20), unique=True, nullable=False)
	description = db.Column(db.String(1000), nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	_phone_number = db.Column(db.Unicode(255), nullable=False)
	phone_country_code = db.Column(db.Unicode(8))
	phone_number = db.orm.composite(PhoneNumber, _phone_number, phone_country_code)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	orders = db.relationship(
		"Order", secondary=OrderSuppliers, back_populates="suppliers", uselist=True
	)


class OrderGroup(db.Model, CRUDMixin):
	__tablename__ = "ordergroup"
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
	owner = db.Column(db.Integer, db.ForeignKey("users.id"))
	members = db.relationship(
		"OrderGroupRole", secondary=OrderGroupMembers, uselist=True
	)

class OrderGroupRole(db.Model, CRUDMixin):
	__tablename__ = "ordergrouprole"
	id = db.Column(db.Integer, primary_key=True)
	ordergroup_id = db.Column(db.Integer, db.ForeignKey("ordergroup.id"))
	user = db.Column(db.Integer, db.ForeignKey("users.id"))
	role = db.Column(
		db.Enum(OrderGroupRoleStatus),
		default=OrderGroupRoleStatus.contributor
	)    

class Order(db.Model, CRUDMixin, fs_mixin):
	__tablename__ = "order"
	# I have o make a correction and create orders for vendors whicj=h eand dropping thee database.
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	owner = db.Column(db.Integer, db.ForeignKey("users.id"))
	contributors = db.relationship(
		"User", secondary=UserOrder, back_populates="orders", uselist=True
	)
	suppliers = db.relationship(
		"Supplier", secondary=OrderSuppliers, back_populates="orders", uselist=True
	)
	vendors = db.relationship(
		"Vendor", secondary=OrderVendors, back_populates="orders", uselist=True
	)
	order_items = db.relationship(
		"OrderItem", secondary=OrderItems, back_populates="orders", uselist=True
	)
	group = db.relationship(
		"OrderGroup", secondary=OrderGroups, backref="order", lazy=True, uselist=False
	)
	status = db.Column(
		db.Enum(OrderStatus),
		default=OrderStatus.planning,
		# nullable=False
	)

	def __repr__(self):
		return f"Order('{self.title}','{self.date_created}')"
	
	def has_access(self, user):
		return user in self.contributors or user in self.suppliers
	
	def can_edit(self,user):
		return user.id in [i.id for i in self.contributors]

	def get_owner(self):
		return User.query.get(self.owner) or None
	
	def add_order(self, title):
		object = OrderItem(title=title, quantity=1)
		object.save()
		self.order_items.append(object)
		self.save()
		return object

	def get_group(self):
		if self.group is None:
			object = OrderGroup.create(order_id=self.id, owner=self.owner)
			self.group = object
			self.save()
			return object
		return self.group
	
	def send_invitation(self,sender_id, recipient_id):
		sender = User.get(sender_id)
		recipient = User.get(recipient_id)
		if sender and recipient:
			if self.group is None:
				new_group = OrderGroup.create(order_id=self.id, owner=sender.id)
				self.group = new_group
				self.save()
			Invitation.create(
				name=self.title,
				sender_id=sender.id,
				receiver_id=recipient.id,
				group_id=self.group.id
			)


class OrderItem(db.Model, CRUDMixin):
	__tablename__ = "orderitem"

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	price = db.Column(SqliteDecimal(scale=2))
	vendors = db.relationship(
		"Vendor", secondary=OrderItemsVendor, back_populates="order_items", uselist=True
	)
	orders = db.relationship(
		"Order", secondary=OrderItems, back_populates="order_items", uselist=False
	)
	description = db.Column(db.String(1000), nullable=True)
	# remembet to change null to false after resetting this table
	date_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
	measure = db.Column(db.Integer, db.ForeignKey("measure.id"))
	measure_quantity = db.Column(SqliteDecimal(scale=2))
	measurement_type = db.Column(
		db.Enum(MeasurementType),
		default=MeasurementType.measure,
	)

	
	def __repr__(self):
		return f"Order Item ('{self.title}','{self.date_created}')"


class ItemSchema(ma.SQLAlchemySchema):
# pip install marshmallow_enu
	measurement_type = fields.Enum(MeasurementType)
	
	class Meta:
		model = OrderItem
		fields = [column.name for column in model.__table__.columns]

			

class Orderchema(ma.SQLAlchemyAutoSchema):
	order_items = ma.List(ma.Nested(ItemSchema))
	class Meta:
		model = Order
		exclude = ("status",)



class Measure(db.Model, CRUDMixin):
	__tablename__ = "measure"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=True)


class MeasureSchema(ma.SQLAlchemySchema):
	class Meta:
		fields = ('id', 'name')
		model = Measure


class Request(db.Model):
	__tablename__ = "request"

	index = db.Column(db.Integer, primary_key=True, autoincrement=True)
	response_time = db.Column(db.Float)
	date = db.Column(db.DateTime)
	method = db.Column(db.String)
	size = db.Column(db.Integer)
	status_code = db.Column(db.Integer)
	path = db.Column(db.String)
	user_agent = db.Column(db.String)
	remote_address = db.Column(db.String)
	exception = db.Column(db.String)
	referrer = db.Column(db.String)
	browser = db.Column(db.String)
	platform = db.Column(db.String)
	mimetype = db.Column(db.String)

