# api/v1/services/project_member.py

from api.v1.models.project_member import ProjectMember
from api.db import get_db
from sqlalchemy.orm import Session

class ProjectMemberService:
    
    def create(self, db: Session, **kwargs):
        """Create a new project member."""
        try:
            project_member = ProjectMember(**kwargs)
            db.add(project_member)
            db.commit()
            db.refresh(project_member)
            return project_member
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, project_member_id: int):
        """Get a project member by their ID."""
        return db.query(ProjectMember).get(project_member_id)
    
    def get_all(self, db: Session):
        """Get all project members."""
        return db.query(ProjectMember).all()
    
    def update(self, db: Session, project_member_id: int, **kwargs):
        """Update an existing project member."""
        project_member = db.query(ProjectMember).get(project_member_id)
        if project_member:
            for key, value in kwargs.items():
                setattr(project_member, key, value)
            db.commit()
            db.refresh(project_member)
            return project_member
        return None
    
    def delete(self, db: Session, project_member_id: int):
        """Delete a project member."""
        project_member = db.query(ProjectMember).get(project_member_id)
        if project_member:
            db.delete(project_member)
            db.commit()
            return True
        return False

# Assigning the service to a variable
project_member_service = ProjectMemberService()
