# api/v1/services/role.py

from api.v1.models.role import Role
from api.db import get_db
from sqlalchemy.orm import Session

class RoleService:
    
    def create(self, db: Session, **kwargs):
        """Create a new role."""
        try:
            role = Role(**kwargs)
            db.add(role)
            db.commit()
            db.refresh(role)
            return role
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, role_id: int):
        """Get a role by its ID."""
        return db.query(Role).get(role_id)
    
    def get_all(self, db: Session):
        """Get all roles."""
        return db.query(Role).all()
    
    def update(self, db: Session, role_id: int, **kwargs):
        """Update an existing role."""
        role = db.query(Role).get(role_id)
        if role:
            for key, value in kwargs.items():
                setattr(role, key, value)
            db.commit()
            db.refresh(role)
            return role
        return None
    
    def delete(self, db: Session, role_id: int):
        """Delete a role."""
        role = db.query(Role).get(role_id)
        if role:
            db.delete(role)
            db.commit()
            return True
        return False

# Assigning the service to a variable
role_service = RoleService()
