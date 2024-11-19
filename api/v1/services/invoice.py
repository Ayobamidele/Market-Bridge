# api/v1/services/invoice.py

from api.v1.models.invoice import Invoice
from api.db import get_db
from sqlalchemy.orm import Session

class InvoiceService:
    
    def create(self, db: Session, **kwargs):
        """Create a new invoice."""
        try:
            invoice = Invoice(**kwargs)
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, invoice_id: int):
        """Get an invoice by its ID."""
        return db.query(Invoice).get(invoice_id)
    
    def get_all(self, db: Session):
        """Get all invoices."""
        return db.query(Invoice).all()
    
    def update(self, db: Session, invoice_id: int, **kwargs):
        """Update an existing invoice."""
        invoice = db.query(Invoice).get(invoice_id)
        if invoice:
            for key, value in kwargs.items():
                setattr(invoice, key, value)
            db.commit()
            db.refresh(invoice)
            return invoice
        return None
    
    def delete(self, db: Session, invoice_id: int):
        """Delete an invoice."""
        invoice = db.query(Invoice).get(invoice_id)
        if invoice:
            db.delete(invoice)
            db.commit()
            return True
        return False

# Assigning the service to a variable
invoice_service = InvoiceService()
