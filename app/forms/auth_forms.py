from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from markupsafe import Markup
from models.player import Account


class LoginForm(FlaskForm):
    """Login form for user authentication"""
    
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=20, message='Username must be between 3 and 20 characters')
        ],
        render_kw={
            'placeholder': 'Enter your username',
            'class': 'form-input'
        }
    )
    
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters long')
        ],
        render_kw={
            'placeholder': 'Enter your password',
            'class': 'form-input'
        }
    )
    remember_me = BooleanField(
        'Remember Me',
        render_kw={'class': 'styled'}
    )
    
    submit = SubmitField(
        Markup('Login'),
        render_kw={'class': 'btn btn-blue btn-block btn-large'}
    )
    
    def validate_username(self, username):
        """Custom validator to check if username exists"""
        account = Account.query.filter_by(username=username.data).first()
        if not account:
            raise ValidationError('Invalid username or password.')


class RegisterForm(FlaskForm):
    """Registration form for new users"""
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=20, message='Username must be between 3 and 20 characters')
        ],
        render_kw={
            'placeholder': 'Choose a username',
            'class': 'form-input'
        }
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email is required'),
            Length(min=6, max=50, message='Email must be between 6 and 50 characters')
        ],
        render_kw={
            'placeholder': 'Enter your email',
            'class': 'form-input',
            'type': 'email'
        }
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters long')
        ],
        render_kw={
            'placeholder': 'Create a password',
            'class': 'form-input'
        }
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password')
        ],
        render_kw={
            'placeholder': 'Confirm your password',
            'class': 'form-input'
        }
    )
    
    accept_terms = BooleanField(
        'I accept the Terms and Conditions',
        validators=[DataRequired(message='You must accept the terms and conditions')],
        render_kw={'class': 'styled'}
    )
    
    submit = SubmitField(
        'Register',
        render_kw={'class': 'btn btn-green btn-block btn-large'}
    )
    
    def validate_username(self, username):
        """Check if username is already taken"""
        account = Account.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError('Email already registered. Please use a different email.')
    
    def validate_confirm_password(self, confirm_password):
        """Check if passwords match"""
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords do not match.')
