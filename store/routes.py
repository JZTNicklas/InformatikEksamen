from flask import render_template, redirect, url_for, request, make_response
from store.models import Users, databaseResults, Calendar, Dag, Begivenhed
from store.forms import RegistrationForm, LoginForm
from store import app, db
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from math import ceil

@app.route('/')
@app.route('/home')
def home():
	return render_template("home.html")





@app.route('/signup', methods=["GET","POST"])
def signup():
	form=RegistrationForm()
	if form.validate_on_submit():
		if Users.query.filter_by(username=form.username.data).first():
			return render_template("signup.html", form=form)
		if Users.query.filter_by(email=form.email.data).first():
			return render_template("signup.html", form=form)	
		db.session.add(Users(email=form.email.data,username=form.username.data,password=form.password.data))
		db.session.commit()
		user = Users.query.filter_by(username=form.username.data).first()
		
		db.session.add(Calendar(user_id=user.id))
		db.session.commit()
		cal = Calendar.query.filter_by(user_id=user.id).first()

		for i in range(1,8):
			db.session.add(Dag(calendar_id=cal.id))
			db.session.commit()
			dag = Dag.query.filter_by(calendar_id=cal.id).first()
			db.session.add(Begivenhed(time=ceil(datetime.now().hour),content="Vask hænder!",dag_id=dag.id))
			db.session.commit()

		

		return redirect('/login')
	return render_template("signup.html", form=form)
	
		
	


@app.route('/login', methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user and form.password.data == user.password:
			login_user(user,False)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			return redirect('/home')
	return render_template("login.html", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/home')

