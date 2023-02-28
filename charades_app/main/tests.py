import os
import unittest 
import app

from datetime import date
 
from charades_app.extensions import app, db, bcrypt
from charades_app.models import Word, Category, User

"""
Run these tests with the command:
python3 -m unittest charades_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

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

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the books show up on the homepage."""

        create_word()
        create_category()
        create_user()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)


        self.assertNotIn('Log Out', response_text)
        self.assertNotIn('Play Game', response_text)
        self.assertNotIn('Contribute to Game Database', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the books show up on the homepage."""

        create_word()
        create_category()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('me1', response_text)
        self.assertIn('Play Game', response_text)
        self.assertIn('Contribute to Game Database', response_text)
        self.assertIn('Log Out', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)


    def test_contribute_page_logged_in(self):
        """Test that the book appears on its detail page."""
        create_word()
        create_category()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/contribute', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("Birds", response_text)
        self.assertIn("Add Word", response_text)
        self.assertIn("Edit Word", response_text)

