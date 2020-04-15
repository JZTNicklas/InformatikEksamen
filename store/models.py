from store import db, login_manager
from flask_table import Table, Col
from flask_login import UserMixin
from datetime import datetime, date
from math import ceil


@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String)
	username = db.Column(db.String, unique=True)
	admin = db.Column(db.Boolean,default=False)
	calendar = db.relationship("Calendar",backref="user",lazy=True)

	def __repr__(self):
		return self.email

	def getPassword(self):
		return self.password

	def isAdmin(self):
		return self.admin

class Calendar(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dag = db.relationship("Dag",backref="calendar",lazy=True)
	#custom_dag = db.relationship("CustomDag",backref="calendar",lazy=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	
	def __repr__(self):
		return str(self.user_id)


class Dag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Integer, default=datetime.now().isoweekday())
	begivenhed = db.relationship("Begivenhed",backref="dag",lazy=True)
	calendar_id = db.Column(db.Integer, db.ForeignKey("calendar.id"), nullable=False)
	
	def __repr__(self):
		return str(self.calendar_id)


class Begivenhed(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.Integer, default=int(ceil(datetime.now().hour)))
	content = db.Column(db.String)
	dag_id = db.Column(db.Integer, db.ForeignKey("dag.id"), nullable=False)
	def __repr__(self):
		return str(self.content)
'''class CustomDag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Integer, default=datetime.now().isoweekday())
	begivenhed = db.relationship("CustomBegivenhed",backref="dag",lazy=True)
	begivenhed_id = db.Column(db.Integer, db.ForeignKey("calendar.id"), nullable=False)

class CustomBegivenhed(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.DateTime, default=ceil(datetime.now().hour))
	content = db.Column(db.String, nullable=False)
	begivenhed_id = db.Column(db.Integer, db.ForeignKey("customDag.id"), nullable=False)
'''

class databaseResults(Table):
    id = Col('id', show=False)
    name = Col('Name')
    price = Col('Price')
    stock = Col('Stock')
