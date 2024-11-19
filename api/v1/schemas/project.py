from marshmallow import Schema, fields
from marshmallow import Schema, fields
from api.v1.schemas.project_member import ProjectMemberResponse
from api.v1.schemas.invoice import InvoiceResponse



class ProjectCreate(Schema):
    name = fields.String(required=True)  # Project name
    description = fields.String(required=False, allow_none=True)  # Optional description
    type = fields.String(required=True, validate=lambda x: x in ['personal', 'business'])  # Type, must be 'personal' or 'business'
    owner_id = fields.String(required=True)  # The owner (user) of the project

    # Meta class can be used to specify fields
    class Meta:
        fields = ('name', 'description', 'type', 'owner_id')


class ProjectResponse(Schema):
    id = fields.String(dump_only=True)  # Project ID (generated automatically)
    name = fields.String(dump_only=True)  # Project name
    description = fields.String(dump_only=True)  # Description
    type = fields.String(dump_only=True)  # Type ('personal' or 'business')
    owner_id = fields.String(dump_only=True)  # The owner (user) of the project
    members = fields.Nested(ProjectMemberResponse, many=True, dump_only=True)  # Nested members related to the project
    invoices = fields.Nested(InvoiceResponse, many=True, dump_only=True)  # Nested invoices related to the project

    class Meta:
        fields = ('id', 'name', 'description', 'type', 'owner_id', 'members', 'invoices')