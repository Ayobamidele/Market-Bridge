from flask import Blueprint, render_template

# Create a Blueprint for the home section
home_pages = Blueprint('home_pages', __name__, template_folder='templates')

@home_pages.route('/', methods=['GET'])
def home():
    """
    Render the home page.
    """
    return render_template('home.html', title="Home")

@home_pages.route('/about', methods=['GET'])
def about():
    """
    Render the about page.
    """
    return render_template('about.html', title="About")
