# api/v1/services/invoice_item.py

from api.v1.models.invoice_item import InvoiceItem
from api.db import get_db
from sqlalchemy.orm import Session

class InvoiceItemService:
    
    def create(self, db: Session, **kwargs):
        """Create a new invoice item."""
        try:
            invoice_item = InvoiceItem(**kwargs)
            db.add(invoice_item)
            db.commit()
            db.refresh(invoice_item)
            return invoice_item
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, invoice_item_id: int):
        """Get an invoice item by its ID."""
        return db.query(InvoiceItem).get(invoice_item_id)
    
    def get_all(self, db: Session):
        """Get all invoice items."""
        return db.query(InvoiceItem).all()
    
    def update(self, db: Session, invoice_item_id: int, **kwargs):
        """Update an existing invoice item."""
        invoice_item = db.query(InvoiceItem).get(invoice_item_id)
        if invoice_item:
            for key, value in kwargs.items():
                setattr(invoice_item, key, value)
            db.commit()
            db.refresh(invoice_item)
            return invoice_item
        return None
    
    def delete(self, db: Session, invoice_item_id: int):
        """Delete an invoice item."""
        invoice_item = db.query(InvoiceItem).get(invoice_item_id)
        if invoice_item:
            db.delete(invoice_item)
            db.commit()
            return True
        return False

# Assigning the service to a variable
invoice_item_service = InvoiceItemService()
