import os
from unittest import TestCase
import app

from datetime import date
 
from charades_app.extensions import app, db, bcrypt
from charades_app.models import Word, Category, User

"""
Run these tests with the command:
python3 -m unittest charades_app.auth.tests
"""

#################################################
# Setup
#################################################

def create_word():
    c1 = Category(name='Animal')
    w1 = Word(
        name='Elephant',
        hint='Large mammal, has a trunk',
        category=c1
    )
    db.session.add(c1)
    db.session.add(w1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
        username='me1', 
        password=password_hash, 
        firstname='Blah', 
        lastname='Halb',
        email = 'blah.halb@gmail.com')
    db.session.add(user)
    db.session.commit()

def create_category():
    c1 = Category(name='Birds')
    db.session.add(c1)
    db.session.commit()


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            "username": "Vitavita",
            "password": "passpass",
            "firstname":'Blah', 
            "lastname": 'Halb',
            "email": 'blah.halb@gmail.com'
        }
        self.app.post('/signup', data=post_data, follow_redirects=True)
        created_user = User.query.filter_by(username="Vitavita").one()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "Vitavita")

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password',
            "firstname":'Blah', 
            "lastname": 'Halb',
            "email": 'blah.halb@gmail.com'
        }
        self.app.post('/signup', data=post_data, follow_redirects=True)
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password',
        }
        response = self.app.post('/login', data=post_data, follow_redirects = True)
        response_text = response.get_data(as_text=True)
        self.assertNotIn('Log In', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'randononex',
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data, follow_redirects = True)
        response_text = response.get_data(as_text=True)
        self.assertIn("No user with that username. Please try again.", response_text)
        

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'nonexpass'
        }
        response = self.app.post('/login', data=post_data, follow_redirects = True)
        response_text = response.get_data(as_text=True)
        self.assertIn("Password does not match. Please try again.", response_text)

    def test_logout(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'nonexpass'
        }
        self.app.post('/login', data=post_data, follow_redirects = True)
        response = self.app.get('/logout', follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
