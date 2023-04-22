import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '187fcfbbef3b4af9e3dfeba2afd51e7b'
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    # BOOTSTRAP_BOOTSWATCH_THEME = 'yeti'
    # Email Configuration
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "ayobamideleewetuga@zohomail.com"
    MAIL_PASSWORD = "ivh1BVwVDVpt"
    ADMINS = ['ayobamideleewetuga@zohomail.com']
    SERVER_EMAIL = "ayobamideleewetuga@zohomail.com"