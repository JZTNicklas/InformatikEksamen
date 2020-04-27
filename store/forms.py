from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange
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
	dag = IntegerField("dag")
	time = IntegerField("time")
	content = StringField("content")
	submit = SubmitField("Log ind")

''', validators=[DataRequired(),NumberRange(min=0,max=6)]'''