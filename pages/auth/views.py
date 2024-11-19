# pages/auth/__init__.py
from flask import render_template, Blueprint
from api.v1.forms import LoginForm
# Create a Blueprint for the pages in the 'auth' section
auth_pages = Blueprint('auth_pages', __name__, template_folder='templates')

# Route for the registration page (GET request)
@auth_pages.route('/register', methods=['GET'])
def register():
    form = LoginForm()
    return render_template('register.html', form=form)  # Rendering the registration template

# Route for the login page (GET request)
@auth_pages.route('/login', methods=['GET'])
def login():
    return render_template('login.html')  # Rendering the login template

# Route for the password reset request page (GET request)
@auth_pages.route('/password_reset', methods=['GET'])
def password_reset_request_page():
    return render_template('reset_password_request.html')  # Rendering the password reset request page

# Route for the password reset page (GET request)
@auth_pages.route('/reset_password/<token>', methods=['GET'])
def reset_password_page(token):
    return render_template('reset_password.html', token=token)  # Rendering the reset password page

# Register the Blueprint with the app
# def register_auth_pages(app):
#     app.register_blueprint(auth_pages, url_prefix='/auth')
