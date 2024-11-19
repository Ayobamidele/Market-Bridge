from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from api.v1.models import User
from api.v1.services.email import send_password_reset_email
from api.v1.schemas.user import UserCreate
from api.db import db
from werkzeug.security import generate_password_hash
from api.v1.schemas import validate_schema


# Create a Blueprint for the authentication API
auth = Blueprint('auth', __name__, url_prefix="/auth")

# User Registration (POST) - Handles the creation of new users
@auth.route('/register', methods=['POST'])
@validate_schema(UserCreate())
def register(validated_data):
    # At this point, validated_data is already validated
    if User.query.filter_by(email=validated_data['email']).first():
        return jsonify({"message": "Email already registered!"}), 400

    # Create the new user from validated data
    new_user = User(
        firstname=validated_data['firstname'],
        lastname=validated_data['lastname'],
        email=validated_data['email'],
        password=validated_data['password']  # Don't forget to hash the password in a real app!
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

# # User Login (POST) - Handles user login
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     # Validate login credentials
#     schema = UserLogin()
#     errors = schema.validate(data)
#     if errors:
#         return jsonify(errors), 400

#     user = User.query.filter_by(email=data['email']).first()
#     if not user or not user.check_password(data['password']):
#         return jsonify({"message": "Invalid email or password"}), 401

#     # Log the user in
#     login_user(user)
#     return jsonify({
#         "message": "Login successful",
#         "user": user.email
#     })


# # User Logout (POST) - Handles user logout
# @auth_bp.route('/logout', methods=['POST'])
# @login_required
# def logout():
#     logout_user()
#     return jsonify({"message": "Logout successful"})


# # Password Reset Request (POST) - Sends an email with a reset token
# @auth_bp.route('/password_reset', methods=['POST'])
# def password_reset_request():
#     data = request.get_json()
#     schema = ResetPassword()
#     errors = schema.validate(data)
#     if errors:
#         return jsonify(errors), 400

#     user = User.query.filter_by(email=data['email']).first()
#     if user:
#         send_password_reset_email(user)  # Sends the password reset email
#         return jsonify({"message": "Password reset instructions have been sent to your email."}), 200
#     return jsonify({"message": "Email not found"}), 404


# # Reset Password (POST) - Allows the user to reset the password using the token
# @auth_bp.route('/reset_password/<token>', methods=['POST'])
# def reset_password(token):
#     data = request.get_json()
#     schema = ResetPassword()
#     errors = schema.validate(data)
#     if errors:
#         return jsonify(errors), 400

#     user = User.verify_reset_password_token(token)
#     if not user:
#         return jsonify({"message": "Invalid or expired token"}), 400

#     user.set_password(data['password'])
#     db.session.commit()

#     return jsonify({"message": "Password has been reset successfully"}), 200
