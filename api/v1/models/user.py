from sqlalchemy import Column, String, Boolean
from api.v1.models.base import BaseTableModel

class User(BaseTableModel):
	"""User model."""
	__tablename__ = 'users'

	name = Column(String(100), nullable=False)
	email = Column(String(120), unique=True, nullable=False)
	password = Column(String(255), nullable=False)
	username = Column(String(50), unique=True, nullable=False)  
	profile_picture = Column(String, nullable=True)
	phone_number = Column(String(15), unique=True, nullable=True)
	is_active = Column(Boolean, default=True)
	is_admin = Column(Boolean, default=False)
	
