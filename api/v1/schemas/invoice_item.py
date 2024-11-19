from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length, Range

# Schema for creating an invoice item
class InvoiceItemCreate(Schema):
    invoice_id = fields.Str(required=True)
    description = fields.Str(required=True, validate=Length(min=1))
    quantity = fields.Int(required=True, validate=Range(min=1))
    unit_price = fields.Float(required=True, validate=Range(min=0))
    total_price = fields.Float(required=True, validate=Range(min=0))
    
    class Meta:
        unknown = EXCLUDE



# Schema for invoice item response (to return item data)
class InvoiceItemResponse(Schema):
    id = fields.Str()
    invoice_id = fields.Str()
    description = fields.Str()
    quantity = fields.Int()
    unit_price = fields.Float()
    total_price = fields.Float()

    class Meta:
        unknown = EXCLUDE
