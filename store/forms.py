from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from store.models import Users

class RegistrationForm(FlaskForm):
	username = StringField("username", validators=[DataRequired(), Length(min=3,max=15)])
	email = StringField("email", validators=[DataRequired(), Email()])
	password = StringField("password", validators=[DataRequired()])
	submit = SubmitField("Sign up")



class LoginForm(FlaskForm):
	username = StringField("username", validators=[DataRequired()])
	password = StringField("password", validators=[DataRequired()])
	submit = SubmitField("Log in")