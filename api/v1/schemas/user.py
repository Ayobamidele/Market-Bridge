# api/v1/schemas/user.py

from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length, Email, Regexp

# Schema for creating a new user
class UserCreate(Schema):
    username = fields.Str(required=True, validate=Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8))
    is_active = fields.Bool(default=True)
    is_admin = fields.Bool(default=False)
    profile_picture = fields.Str(default=None)
    phone_number = fields.Str(
        required=True, 
        validate=Regexp(r'^\+?1?\d{9,15}$', error="Invalid phone number format")
    )

    class Meta:
        unknown = EXCLUDE


# Schema for user response (for registering or returning user data)
class UserResponse(Schema):
    id = fields.Str()
    username = fields.Str()
    email = fields.Email()
    is_active = fields.Bool()
    is_admin = fields.Bool()
    profile_picture = fields.Str()
    phone_number = fields.Str()

    class Meta:
        unknown = EXCLUDE
