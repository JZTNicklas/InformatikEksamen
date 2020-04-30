'''
Under hver route defineres en funktion som siger hvad der skal ske når den specifikke route bliver requestet.
Skal altid return noget; for det meste: 
render_template(): viser den givne Jinja2 template(html filer mm.)
redirect(): redirecter til en anden route, som efterfølgende køres
'''

#Mange imports er fordi koden er delt op i flere filer i samme package. Det der skal bruges flere steder importeres så fra vores "store" package
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
	idag = date.today() #Få dagens date object, til senere brug
	dage = ["Mandag","Tirsdag","Onsdag","Torsdag","Fredag","Lørdag","Søndag"]
	table = ""
	#Hvis man er logget ind, hent listen over begivenheder der skal ske idag, og lav et html Table der skal vises
	if current_user.is_authenticated:
		begivenhedList = Begivenhed.query.filter_by(dag_id=idag.isoweekday()+((current_user.id-1)*7)) #Query databasen med begivenheder. 
		table = calendarTable(begivenhedList)
		return render_template("home.html",dag=dage[idag.isoweekday()-1], date=idag.day,month=idag.month, table=table) #Render 'home.html', giv dagens dato og måned og tabellen over begivenheder
	else: #Hvis man ikke er logget ind, redirect til /login
		return redirect('/login')


@app.route('/signup', methods=["GET","POST"])
def signup():
	form = RegistrationForm()
	if form.validate_on_submit():
		#Hvis enten username eller email allerede findes i databasen, abort signup og return et redirect for at prøve igen
		if Users.query.filter_by(username=form.username.data).first():
			return render_template("signup.html", form=form)
		if Users.query.filter_by(email=form.email.data).first():
			return render_template("signup.html", form=form)	
		db.session.add(Users(email=form.email.data,username=form.username.data,password=bc.generate_password_hash(form.password.data).decode("utf-8")))
		db.session.commit()
		user = Users.query.filter_by(username=form.username.data).first() #Hvis ingen statements bliver ramt, lav en ny User i databasen, og assign dem til user variablen 
		db.session.add(Calendar(user_id=user.id))
		db.session.commit()
		cal = Calendar.query.filter_by(user_id=user.id).first() #Lav en ny kalender, som hører sammen med den nye users id som foreignkey, og assign dem til cal variablen
		for i in range(7): #Lav 7 dage i kalenderen, som alle har cals id som foreignkey, og assign dem til dag variablen
			db.session.add(Dag(calendar_id=cal.id))
			db.session.commit()
			dag = Dag.query.filter_by(calendar_id=cal.id)[i]
			for j in range(24):
				db.session.add(Begivenhed(time=str(j)+":00",content="",dag_id=dag.id))#For hver dag i kalenderen, lav 24 begivenheder uden content, så de eksistere i databasen. Tiden bliver sat til mellem 00:00 og 23:00
			db.session.commit()
		return redirect('/login') #Hvis alt er gået godt, return et redirect til /login, hvor brugeren nu kan logge ind
	return render_template("signup.html", form=form) #Hvis formen ikke er valid, render 'signup.html'
	

@app.route('/login', methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first() #Hvis formen er valid, find den user i databasen som har den givne email
		if user and bc.check_password_hash(user.password, form.password.data): #Hvis useren findes, og passwordet giver samme hash som det gemt i databasen   
			login_user(user,False) #Login den givne user, remember me=False
			return redirect('/home') #return et redirect til /home efter login er succesfuldt
	return render_template("login.html", form=form) #Hvis formen ikke er valid, render 'login.html', giv form som skal renderes


@app.route('/logout')
def logout():
	logout_user() #Logout user
	return redirect('/login')

@app.route('/change', methods=["GET","POST"])
def change():
	form = ChangeForm()
	if form.validate_on_submit(): #Hvis formen er valid
		user = Users.query.filter_by(email=current_user.email).first() #Definer hvilken user der er logget ind
		cal = Calendar.query.filter_by(user_id=user.id).first() #Bruger user.id til at finde userens kalender
		dag = Dag.query.filter_by(calendar_id=cal.id).all()[form.dag.data-1] #Find dagen der skal redigeres, udfra inputtet i formen
		begivenhed = Begivenhed.query.filter_by(dag_id=dag.id).all()[form.time.data] #Find begivenheden der skal redigres, udfra inputtet i formen
		begivenhed.content = form.content.data #Lav begivenhedens content om til inputtet i formen 
		db.session.commit() #Gem i databasen
		return redirect('/home') #Return et redirect til '/home'
	return render_template("change.html", form=form) #Render 'change.html', giv form som form