import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

class Config(object):
    # Project
    Project_Name = os.getenv('PROJECT_NAME')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "postgresql")
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    
    # Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Use a default secret if not set

    # CSRF Settings
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.zoho.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't', 'y', 'yes']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True').lower() in ['true', '1', 't', 'y', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = os.getenv('ADMINS', '').split(',')
    SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'default_email@example.com')


config = Config()