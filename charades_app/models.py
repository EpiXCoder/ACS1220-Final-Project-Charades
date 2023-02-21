"""Create database models to represent tables."""
from sqlalchemy import ARRAY
from charades_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Word(db.Model):
  """Word model"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  hint = db.Column(db.String(300), nullable=False)

  # The category the word belongs to
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  category = db.relationship('Category', secondary='word_category')
  
  def __str__(self):
      return f'<Word: {self.name}>'

  def __repr__(self):
      return f'<Word: {self.name}>'

class Category(db.Model):
  """Category model"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  word = db.relationship(
      'Word', secondary='word_category')

  def __str__(self):
      return f'<Category: {self.name}>'

  def __repr__(self):
      return f'<Category: {self.name}>'

word_category_table = db.Table('word_category',
  db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
  db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)

class Gameinstance(db.Model):
  """Game Instance model"""
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', secondary='user_gameinstance')
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  category = db.Column(db.String, db.ForeignKey('category.name'), nullable=False)
  # word_array = db.Column(ARRAY(db.String), nullable = False)

  def __repr__(self):
      return f'<GameInstance: {self.id}>'

user_gameinstance_table = db.Table('user_gameinstance',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('gameinstance_id', db.Integer, db.ForeignKey('gameinstance.id')),
)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  firstname = db.Column(db.String(80), nullable=False)
  lastname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  gameinstance_id = db.Column(db.Integer, db.ForeignKey('gameinstance.id'), nullable=False)
  gameinstance = db.relationship('Gameinstance', secondary='user_gameinstance')

  def __repr__(self):
      return f'<User: {self.username}>'


