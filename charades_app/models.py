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

  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
  category = db.relationship('Category', back_populates = 'word')
 
  def __str__(self):
      return f'<Word: {self.name}>'

  def __repr__(self):
      return f'Word(word={self.name}, category={self.category})'

class Category(db.Model):
  """Category model"""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  word = db.relationship('Word', back_populates = 'category')


  def __str__(self):
      return f'{self.name}'

  def __repr__(self):
      return f'Category(name={self.name})'


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  firstname = db.Column(db.String(80), nullable=False)
  lastname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(100), nullable=False)

  def __repr__(self):
      return f'<User: {self.id}>'


