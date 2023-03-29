#!/usr/bin/env python
from datetime import datetime, timedelta
from flask_testing import TestCase
from supply_bridge import app, db
from supply_bridge.models import User
from supply_bridge.config import Config
from sqlalchemy_utils import PhoneNumber
from flask_login import login_user


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class UserModelCase(TestCase):
    """A base test for authentication."""
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['LIVESERVER_PORT'] = 0
        WTF_CSRF_ENABLED = False
        app.config['CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(firstname='Joe', lastname="Regan", email='joe@joes.com',)
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_users_registration(self):
        user = User(firstname='Joe', lastname="Regan", email='joe@joes.com',phone_number=PhoneNumber('08093456822', 'NG'))
        user.set_password("test1234589")
        user.set_username()
        db.session.add(user)
        self.setUp()
        users = User.query.all()
        assert user in users

    def test_login(self):
        user = User(firstname='Joe', lastname="Regan", email='joe@joewwss.com',phone_number=PhoneNumber('08093456822', 'NG'))
        user.set_password("test1234589")
        db.session.add(user)
        self.setUp()
        self.assertTrue(login_user(user))

    

