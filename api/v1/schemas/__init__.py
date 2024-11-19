from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Load and validate the incoming JSON data using the provided schema
                data = schema.load(request.get_json())
            except ValidationError as err:
                # If validation fails, return a 400 response with the validation errors
                return jsonify({"errors": err.messages}), 400
            
            # Pass the validated data to the route function
            return func(data, *args, **kwargs)
        return wrapper
    return decorator
