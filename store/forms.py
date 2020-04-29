'''
Alle forms bliver defineret som klasser. Forms bliver omdannet til html forms når de bliver renderet,
og bliver derfor brugt som vores primære input kilder
'''


#Mange imports er fordi koden er delt op i flere filer i samme package. Det der skal bruges flere steder importeres så fra vores "store" package
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange, InputRequired
from store.models import Users

class RegistrationForm(FlaskForm):
	username = StringField("username", validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField("email", validators=[DataRequired(), Email()])
	password = PasswordField("password", validators=[DataRequired()])
	submit = SubmitField("Tilmeld")

class LoginForm(FlaskForm):
	email = StringField("email", validators=[DataRequired()])
	password = PasswordField("password", validators=[DataRequired()])
	submit = SubmitField("Log ind")

class ChangeForm(FlaskForm):
	dag = IntegerField("dag", validators=[DataRequired(), NumberRange(min=1,max=7)])
	time = IntegerField("time", validators=[InputRequired(), NumberRange(min=0,max=23)])
	content = StringField("content")
	submit = SubmitField("Gem")