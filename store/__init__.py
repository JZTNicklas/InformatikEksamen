'''
__init__.py laver 'store' mappen om til en Python-package. __init__ bruges til at initialisere alle tingene
der skal bruges til hjemmesiden. 

Appen, databasen, loginmanager, Bcrypt til hashing osv.
'''

#Mange imports er fordi koden er delt op i flere filer i samme package. Det der skal bruges flere steder importeres så fra vores "store" package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bc = Bcrypt(app)

from store import routes