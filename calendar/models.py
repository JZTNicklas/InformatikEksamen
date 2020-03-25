from calendar import db, login_manager
from flask_table import Table, Col
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	username = db.Column(db.String, unique=True)
	admin = db.Column(db.Boolean,default=False)

	def __repr__(self):
		return self.email

	def getPassword(self):
		return self.password

	def isAdmin(self):
		return self.admin

