'''
Database modeller og table modeller defineres som klasser i denne fil
Databasen gemmer så instanser af disse klasser 

def __repr__() bliver kaldt hver gang man print et objekt. I stedet for __main__.User object at 0x00C47190 
som ikke kan bruges til noget, print den noget brugbart information som gør det nemmere at identificere objekter
'''


#Mange imports er fordi koden er delt op i flere filer i samme package. Det der skal bruges flere steder importeres så fra vores "store" package
from store import db, login_manager
from flask_table import Table, Col
from flask_login import UserMixin
from datetime import datetime, date
from math import ceil

#Login manager for at vide hvordan den skal kende forskel på users. Giver den det unikke id, som også er primary key
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
	time = db.Column(db.String)
	content = db.Column(db.String)
	dag_id = db.Column(db.Integer, db.ForeignKey("dag.id"), nullable=False)
	def __repr__(self):
		return str(self.content)


#Klassen der definere hvordan tabellen i vores kaldener ser ud. 3 kolonner, hvor kun 2 vises. Tiden og begivenheden 
class calendarTable(Table):
    id = Col('id', show=False)
    time = Col("Tid")
    content = Col('Din Kalender')
    
