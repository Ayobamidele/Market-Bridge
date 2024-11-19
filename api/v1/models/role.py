from api.db import db
from sqlalchemy import Column, String

class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(db.Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'
