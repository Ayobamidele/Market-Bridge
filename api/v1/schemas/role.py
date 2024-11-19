from marshmallow import Schema, fields


class RoleCreateSchema(Schema):
    name = fields.String(required=True)  # The name of the role (must be unique)

    class Meta:
        fields = ('name',)


class RoleResponseSchema(Schema):
    id = fields.Integer(dump_only=True)  # Unique ID of the role (auto-generated)
    name = fields.String(dump_only=True)  # Name of the role

    class Meta:
        fields = ('id', 'name')