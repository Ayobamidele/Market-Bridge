from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length, Range

# Schema for creating an invoice
class InvoiceCreate(Schema):
    user_id = fields.Str(required=True)
    invoice_number = fields.Str(required=True, validate=Length(min=5))
    date_issued = fields.Date(required=True)
    due_date = fields.Date(required=True)
    total_amount = fields.Float(required=True, validate=Range(min=0))
    status = fields.Str(default="pending", validate=Length(min=3))
    
    class Meta:
        unknown = EXCLUDE


# Schema for invoice response (to return the invoice data)
class InvoiceResponse(Schema):
    id = fields.Str()
    user_id = fields.Str()
    invoice_number = fields.Str()
    date_issued = fields.Date()
    due_date = fields.Date()
    total_amount = fields.Float()
    status = fields.Str()

    class Meta:
        unknown = EXCLUDE
