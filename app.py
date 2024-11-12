import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# true -> recreates db
# false -> connects to existing db
recreate = True

# Determine the absolute path of our database file
scriptdir = os.path.abspath(os.path.dirname(__file__))
dbpath = os.path.join(scriptdir, 'freeGamesList.sqlite3')

# Configure the Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Getting the database object handle from the app
db = SQLAlchemy(app)

# TODO define Model for Users
class Users(db.Model):
    __tablename__ = 'Users'
    

# TODO define Model for Games
class Game(db.Model):
    __tablename__ = 'Games'
    

# TODO define Model for Forums
class Forum(db.Model):
    __tablename__ = 'Forums'
    

if recreate:
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # TODO fill with API data


# TODO stub different functions