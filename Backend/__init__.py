from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__,template_folder='../Frontend/templates', static_url_path='/static')
app.config['SECRET_KEY'] = 'c7ec680eb5c98b3c720a90f6732e05cc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


import routes