from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from charades_app.models import Word, User, Category

class WordForm(FlaskForm):
    """Form to create a word"""
    name = StringField('Word',
        validators=[DataRequired(), Length(min=1, max=100)])
    hint = StringField('Hints for Word', 
        validators=[DataRequired(), Length(min=1, max=500)])
    category = QuerySelectField('Category',
        query_factory=lambda: Category.query.all(), get_label = 'name', allow_blank=False)
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    """Form to create a Category"""
    name = StringField('Category',
        validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Submit')


