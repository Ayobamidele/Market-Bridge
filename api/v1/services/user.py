# api/v1/services/user.py

from api.v1.models.user import User
from api.db import get_db
from sqlalchemy.orm import Session

class UserService:
    
    def create(self, db: Session, **kwargs):
        """Create a new user."""
        try:
            user = User(**kwargs)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, user_id: int):
        """Get a user by their ID."""
        return db.query(User).get(user_id)
    
    def get_all(self, db: Session):
        """Get all users."""
        return db.query(User).all()
    
    def update(self, db: Session, user_id: int, **kwargs):
        """Update an existing user."""
        user = db.query(User).get(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user
        return None
    
    def delete(self, db: Session, user_id: int):
        """Delete a user."""
        user = db.query(User).get(user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

# Assigning the service to a variable
user_service = UserService()
