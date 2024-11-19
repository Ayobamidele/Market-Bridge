from sqlalchemy import Column, String, Enum, ForeignKey, UniqueConstraint
from api.v1.models.base import BaseTableModel
from enum import Enum as PyEnum

class RoleType(PyEnum):
    """Enum for project member roles."""
    READ = 'read'
    EDIT = 'edit'
    ADMIN = 'admin'

class ProjectMember(BaseTableModel):
    """Project Member model for associating users and projects."""
    __tablename__ = 'project_members'

    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    role = Column(Enum(RoleType), nullable=False, default=RoleType.READ)  # Simplified role column

    # Unique constraint to ensure a user is not added twice to the same project
    __table_args__ = (
        UniqueConstraint('project_id', 'user_id', name='unique_project_member'),
    )

