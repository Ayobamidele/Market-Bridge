from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from api.v1.models.base import BaseTableModel

class InvoiceItem(BaseTableModel):
    """Invoice Item model."""
    __tablename__ = 'invoice_items'

    invoice_id = Column(String, ForeignKey('invoices.id'), nullable=False)  # Foreign key to Invoice
    description = Column(String(255), nullable=False)  # Description of the item/service
    unit_price = Column(Numeric(10, 2), nullable=True, default=0.00)  # Unit price of the item (optional)
    quantity = Column(Numeric(10, 2), nullable=False, default=1)  # Quantity of the item/service
    total_price = Column(Numeric(10, 2), nullable=False, default=0.00)  # Total price for this item (calculated)

    # Relationship to Invoice (backref for the invoice this item belongs to)
    invoice = relationship('Invoice', backref='items')

    def calculate_total_price(self):
        """Calculate total price based on unit price and quantity."""
        if self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
        else:
            self.total_price = 0.00  # Default to 0 if unit_price or quantity is not provided
