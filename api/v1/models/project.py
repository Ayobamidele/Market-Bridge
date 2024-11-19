from sqlalchemy import Column, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base import BaseTableModel
from enum import Enum as PyEnum

class ProjectType(PyEnum):
    PERSONAL = 'personal'
    BUSINESS = 'business'

class Project(BaseTableModel):
    """Project model."""
    __tablename__ = 'projects'

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ProjectType), nullable=False)
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)

    # Relationships
    members = relationship('ProjectMember', backref='project', lazy=True)
    invoices = relationship('Invoice', backref='project', lazy=True)
