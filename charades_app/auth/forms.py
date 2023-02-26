from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, email_validator
from charades_app.models import User
from charades_app.extensions import bcrypt

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('First Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    lastname = StringField('Last Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email',
        validators=[DataRequired(), Email("This field requires a valid email address")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        email_address = User.query.filter_by(email=email.data).first()
        if email_address:
            raise ValidationError('That email already exists in our system. Choose a different one or log-in with an existing account.')


class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password does not match. Please try again.')