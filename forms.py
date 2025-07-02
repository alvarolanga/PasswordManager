from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #Username entry
    password = PasswordField('Password', validators=[DataRequired()]) #Password entry
    submit = SubmitField('Login') #Login button

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)]) #Username minimum has to be 3 char
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)]) #Pasword has to be min 6 char
    submit = SubmitField('Register')

class CredentialForm(FlaskForm): #When Logged In, form for the password manager
    service = StringField('Service', validators=[DataRequired()])  #Service Name Space
    username = StringField('Username', validators=[DataRequired()]) #Username for the service
    password = PasswordField('Password', validators=[DataRequired()]) #Password for the service
    submit = SubmitField('Save') #Save credential button
