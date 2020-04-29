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