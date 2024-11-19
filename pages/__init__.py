from flask import Blueprint

# Import all Blueprints from submodules
from pages.auth import auth_pages
from pages.home import home_pages

# Create a Blueprint for `pages`
pages = Blueprint('pages', __name__)

# Register the Blueprints with the `pages` Blueprint
pages.register_blueprint(auth_pages, url_prefix='/auth')
pages.register_blueprint(home_pages, url_prefix='/')

__all__ = ['pages_bp']
