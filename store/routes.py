from flask import render_template, redirect, url_for, request, make_response
from store.models import Items, Users, databaseResults
from store.forms import RegistrationForm, LoginForm
from store import app, db
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/stock')
@login_required
def stock():
	result = Items.query.all()
	table = databaseResults(result)
	return render_template("stock.html", table=table)

@app.route('/addStock')
@login_required
def addStock():
	name = request.args.get("name")
	price = request.args.get("price")
	stock = request.args.get("stock")
	if type(name) == str and type(price) == str and type(stock) == str:
		db.session.add(Items(name=name,price=float(price),stock=int(stock)))
		db.session.commit()
		return redirect('/addStock')
	return render_template("addStock.html")


@app.route('/signup', methods=["GET","POST"])
def signup():
	form=RegistrationForm()
	if form.validate_on_submit():
		if Users.query.filter_by(username=form.username.data).first():
			return render_template("signup.html", form=form)
		if Users.query.filter_by(email=form.email.data).first():
			return render_template("signup.html", form=form)	
		user = Users(email=form.email.data,username=form.username.data,password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect('/login')
	return render_template("signup.html", form=form)
	
		
	


@app.route('/login', methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
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

