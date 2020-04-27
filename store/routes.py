from flask import render_template, redirect, url_for, request, make_response
from store.models import Users, calendarTable, Calendar, Dag, Begivenhed
from store.forms import RegistrationForm, LoginForm
from store import app, db, bc
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from math import ceil

@app.route('/')
@app.route('/home')
def home():
	table = ""
	if current_user.is_authenticated:
		print(current_user.username)
		begivenhedList = Begivenhed.query.filter_by(dag_id=current_user.id)
		table = calendarTable(begivenhedList)
	return render_template("home.html", date=datetime.now().day,month=datetime.now().month, table=table)


@app.route('/signup', methods=["GET","POST"])
def signup():
	form=RegistrationForm()
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
			
			dag = Dag.query.filter_by(calendar_id=cal.id)[i]
			db.session.add(Begivenhed(time="00:00",content="Vask hænder!",dag_id=dag.id))
			for j in range(1,24):
				#Laver 23 begivenheder uden content, bare så de eksistere i databasen
				db.session.add(Begivenhed(time=str(j)+":00",content="",dag_id=dag.id))
			#Laver en manuel begivenhed med content "Vask hænder!" klokken 24
			db.session.commit()

		return redirect('/login')
	return render_template("signup.html", form=form)
	

@app.route('/login', methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and bc.check_password_hash(user.password, form.password.data):
			login_user(user,False)
			print("Login Succesfull")
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			return redirect('/home')
	return render_template("login.html", form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')

