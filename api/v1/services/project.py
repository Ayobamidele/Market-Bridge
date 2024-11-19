# api/v1/services/project.py

from api.v1.models.project import Project
from api.db import get_db
from sqlalchemy.orm import Session

class ProjectService:
    
    def create(self, db: Session, **kwargs):
        """Create a new project."""
        try:
            project = Project(**kwargs)
            db.add(project)
            db.commit()
            db.refresh(project)
            return project
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, project_id: int):
        """Get a project by its ID."""
        return db.query(Project).get(project_id)
    
    def get_all(self, db: Session):
        """Get all projects."""
        return db.query(Project).all()
    
    def update(self, db: Session, project_id: int, **kwargs):
        """Update an existing project."""
        project = db.query(Project).get(project_id)
        if project:
            for key, value in kwargs.items():
                setattr(project, key, value)
            db.commit()
            db.refresh(project)
            return project
        return None
    
    def delete(self, db: Session, project_id: int):
        """Delete a project."""
        project = db.query(Project).get(project_id)
        if project:
            db.delete(project)
            db.commit()
            return True
        return False

# Assigning the service to a variable
project_service = ProjectService()
