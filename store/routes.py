'''
Under hver route defineres en funktion som siger hvad der skal ske når den specifikke route bliver requestet.
Skal altid return noget; for det meste: 
render_template(): viser den givne Jinja2 template(html filer mm.)
redirect(): redirecter til en anden route
'''

#Mange imports er fordi koden er delt op i flere filer i samme package. Det der skal bruges flere steder importeres så fra "Store" package
from flask import render_template, redirect, url_for, request, make_response
from store.models import Users, calendarTable, Calendar, Dag, Begivenhed
from store.forms import RegistrationForm, LoginForm, ChangeForm
from store import app, db, bc
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from math import ceil




@app.route('/')
@app.route('/home')
def home():
	#Få dagens date object.
	idag = date.today()
	table = ""
	#Hvis man er logget ind, 
	if current_user.is_authenticated:
		begivenhedList = Begivenhed.query.filter_by(dag_id=idag.isoweekday()+((current_user.id-1)*7))
		table = calendarTable(begivenhedList)
		return render_template("home.html", date=idag.day,month=idag.month, table=table)
	else:
		return redirect('/login')


@app.route('/signup', methods=["GET","POST"])
def signup():
	form = RegistrationForm()
	if form.validate_on_submit():
		if Users.query.filter_by(username=form.username.data).first():
			return render_template("signup.html", form=form)
		if Users.query.filter_by(email=form.email.data).first():
			return render_template("signup.html", form=form)	
		db.session.add(Users(email=form.email.data,username=form.username.data,password=bc.generate_password_hash(form.password.data).decode("utf-8")))
		db.session.commit()
		user = Users.query.filter_by(username=form.username.data).first()
		
		db.session.add(Calendar(user_id=user.id))
		db.session.commit()
		cal = Calendar.query.filter_by(user_id=user.id).first()

		for i in range(7):
			db.session.add(Dag(calendar_id=cal.id))
			db.session.commit()
			
			for j in range(24):
				#Laver 24 begivenheder uden content, bare så de eksistere i databasen
				db.session.add(Begivenhed(time=str(j)+":00",content="",dag_id=dag.id))
			db.session.commit()

		return redirect('/login')
	return render_template("signup.html", form=form)
	

@app.route('/login', methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bc.check_password_hash(user.password, form.password.data):
			login_user(user,False)
			print("Login Succesfull")
			return redirect('/home')
	return render_template("login.html", form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')

@app.route('/change', methods=["GET","POST"])
def change():
	form = ChangeForm()
	if form.validate_on_submit():
		print("1")
		user = Users.query.filter_by(email=current_user.email).first()
		cal = Calendar.query.filter_by(user_id=user.id).first()
		dag = Dag.query.filter_by(calendar_id=cal.id).all()[form.dag.data-1]
		begivenhed = Begivenhed.query.filter_by(dag_id=dag.id).all()[form.time.data]
		begivenhed.content = form.content.data
		db.session.commit()
		print("commited")
		return redirect('/home')
	return render_template("change.html", form=form)