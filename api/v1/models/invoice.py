from sqlalchemy import Column, String, Numeric, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from api.v1.models.base import BaseTableModel
from enum import Enum as PyEnum

class InvoiceStatus(PyEnum):
    DRAFT = 'draft'
    SENT = 'sent'
    PAID = 'paid'

class Invoice(BaseTableModel):
    """Invoice model."""
    __tablename__ = 'invoices'

    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    created_by = Column(String, ForeignKey('users.id'), nullable=False)
    invoice_number = Column(String(100), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False, default=0.00)  # Total amount
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    due_date = Column(Date, nullable=True)

    # Relationships
    items = relationship('InvoiceItem', backref='invoice', lazy=True)

    def calculate_total(self):
        """Calculate the total amount based on associated items."""
        self.amount = sum(item.amount for item in self.items)
