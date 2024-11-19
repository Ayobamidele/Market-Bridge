from marshmallow import Schema, fields
from marshmallow.validate import OneOf

class ProjectMemberCreate(Schema):
    project_id = fields.String(required=True)  # The project the member will be associated with
    user_id = fields.String(required=True)  # The user being added to the project
    role = fields.String(required=True, validate=OneOf(['read', 'edit', 'admin']))  # Role for the user in the project

    class Meta:
        fields = ('project_id', 'user_id', 'role')


class ProjectMemberResponse(Schema):
    id = fields.String(dump_only=True)  # Unique ID of the project member
    project_id = fields.String(dump_only=True)  # The associated project ID
    user_id = fields.String(dump_only=True)  # The associated user ID
    role = fields.String(dump_only=True)  # The role of the member in the project (read, edit, admin)

    class Meta:
        fields = ('id', 'project_id', 'user_id', 'role')
