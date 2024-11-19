from flask import Blueprint

# Import individual route Blueprints
from api.v1.routes.auth import auth

# Create a main Blueprint for versioning
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

# Register the Blueprints under the main v1 Blueprint
v1.register_blueprint(auth)

# Export the v1 Blueprint
__all__ = ['v1']
