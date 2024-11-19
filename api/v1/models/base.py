from sqlalchemy import Column, DateTime, String
from api.db.database import Base
from uuid import uuid4
from datetime import datetime

class BaseTableModel(Base):
    """Base model class for all tables with common fields and helper methods."""
    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


    @classmethod
    def get_all(cls):
        """Return all records from the database"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """Return a single record by its ID"""
        return cls.query.get(id)
