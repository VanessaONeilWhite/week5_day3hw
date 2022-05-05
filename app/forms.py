from flask_wtf import FlaskForm
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User


class PokemonForm(FlaskForm):
    pokename= StringField('Enter a Pokemon', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name=StringField('First Name', validators=[DataRequired()]) 
    last_name= StringField('Last Name', validators=[DataRequired()])
    email=StringField('email', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit= SubmitField('Register') 

    def validate_email(form,field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email is Already in Use')