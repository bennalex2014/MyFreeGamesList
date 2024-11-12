"""
INSTALLING REQUIRED PACKAGES
Run the following commands to install all required packages.
python -m pip install --upgrade pip
python -m pip install --upgrade flask-login
"""

###############################################################################
# Imports
###############################################################################
from __future__ import annotations
import os
from datetime import date
from flask import Flask, render_template, url_for, redirect
from flask import request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user

# import urllib library  + json for API 
from urllib.request import urlopen 
import json 

# Import from local package files
from hashers import Hasher
from loginforms import RegisterForm, LoginForm

###############################################################################
# Basic Configuration
###############################################################################

# Identify necessary files
scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "freeGamesList.sqlite3")
pepfile = os.path.join(scriptdir, "pepper.bin")

# open and read the contents of the pepper file into your pepper key
# NOTE: you should really generate your own and not use the one from the starter
with open(pepfile, 'rb') as fin:
  pepper_key = fin.read()

# create a new instance of Hasher using that pepper key
pwd_hasher = Hasher(pepper_key)

# Configure the Flask Application
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'correcthorsebatterystaple'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Getting the database object handle from the app
db = SQLAlchemy(app)

# Prepare and connect the LoginManager to this app
login_manager = LoginManager()
login_manager.init_app(app)
# function name of the route that has the login form (so it can redirect users)
login_manager.login_view = 'get_login' # type: ignore
login_manager.session_protection = "strong"
# function that takes a user id and
@login_manager.user_loader
def load_user(uid: int) -> User|None:
    return User.query.get(int(uid))

###############################################################################
# Database Setup
###############################################################################

# Create a database model for Users
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute
    reviews = db.relationship('Review', backref='user')
    forumComments = db.relationship('ForumComment',backref='user')

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd: str) -> None:
        self.password_hash = pwd_hasher.hash(pwd)
    
    # add a verify_password convenience method
    def verify_password(self, pwd: str) -> bool:
        return pwd_hasher.check(pwd, self.password_hash)

class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    numReviews = db.Column(db.Integer, nullable=False)
    totalRevScore = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='game')
    forumComments = db.relationship('ForumComment',backref='game')

class Review(db.Model):
    __tablename__ = 'Reviews'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Games.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Unicode, nullable=False)

class ForumComment(db.Model):
    __tablename__ = 'ForumComment'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Games.id'), primary_key=True)
    content = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.Date, nullable=False)


#   creates database - set to false after the first run to prevent repeated creation
if True:
    with app.app_context():
        db.drop_all()
        db.create_all()

        owner = User(isAdmin=1,username="Owner",password="ownerowner")
        u1 = User(isAdmin=0,username="User1",password="useruser1")
        u2 = User(isAdmin=0,username="User2",password="useruser2")
        u3 = User(isAdmin=0,username="User3",password="useruser3")
        u4 = User(isAdmin=0,username="User4",password="useruser4")
        
        gamesAPI = "https://www.freetogame.com/api/games"

        response = urlopen(gamesAPI)
        gamesList= json.loads(response.read())

        for game in gamesList:
            game.get("id")
            instance = Game(id=game.get("id"), numReviews=0, totalRevScore=0)
            db.session.add(instance)

        db.session.commit()

        ow2 = game=Game.query.filter_by(id=540).first()
        pubg = game=Game.query.filter_by(id=516).first()
        fallGuys = game=Game.query.filter_by(id=523).first()

        rev1 = Review(user=u1, game=ow2, text="Big downgrade from OW 1. Miss the old days", score = 3)
        rev2 = Review(user=u2, game=ow2, text="MASSIVE MASSIVE downgrade from OW 1. Miss the old days", score = 2)
        rev3 = Review(user=u4, game=pubg, text="downloaded. dropped. beheaded by a butter knife. uninstalled...", score = 2)
        rev4 = Review(user=u4, game=fallGuys, text="I like to fall!", score = 7)
        rev5 = Review(user=u3, game=fallGuys, text="I like being a guy too", score = 8)
        rev6 = Review(user=u3, game=pubg, text="BEST game ever!", score = 10)


        com1 = ForumComment(user=u1,game=ow2, content=bytes("I can put anything in here because of type LargeBinary", 'utf-8'), timestamp=date(2024,11,11))
        com2 = ForumComment(user=u2,game=fallGuys, content=bytes("I can put anything in here because of type LargeBinary", 'utf-8'), timestamp=date(2023,11,11))
        com3 = ForumComment(user=u4,game=fallGuys, content=bytes("I can put anything in here because of type LargeBinary", 'utf-8'), timestamp=date(2022,11,11))
        com4 = ForumComment(user=u3,game=pubg, content=bytes("I can put anything in here because of type LargeBinary", 'utf-8'), timestamp=date(2021,11,11))

        db.session.add_all((owner, u1, u2, u3, u4))
        db.session.add_all((rev1, rev2, rev3, rev4, rev5, rev6))
        db.session.add_all((com1, com2, com3, com4))
        db.session.commit()

# sample query/scratchpad -> set to True to use
if False:
    with app.app_context():
        ow2 = Game.query.filter_by(id=540).first()

        # go through each review for game
        for rev in ow2.reviews:
            print(f"Review: {rev.text} \nScore: {rev.score}/10\n")

###############################################################################
# Route Handlers
###############################################################################

# TODO match functions and html with database
@app.get('/register/')
def get_register():
    form = RegisterForm()
    return render_template('register.html', form=form)

# TODO match functions and html with database
@app.post('/register/')
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if the email address is free, create a new user and send to login
        if user is None:
            user = User(email=form.email.data, password=form.password.data) # type:ignore
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_login'))
        else: # if the user already exists
            # flash a warning message and redirect to get registration form
            flash('There is already an account with that email address')
            return redirect(url_for('get_register'))
    else: # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

# TODO match functions and html with database
@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template('login.html', form=form)

# TODO match functions and html with database
@app.post('/login/')
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        else: # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('get_login'))
    else: # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))


# TODO home
@app.get('/')
def index():
    return render_template('home.html', current_user=current_user)

# TODO match functions and html with database -> redirect to login page -> we do not allow non-logged in users
@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

# TODO Profile page -> get/post

# TODO Edit profile page -> get/post

# TODO Game Page -> including reviews, descriptions, score, etc.

# TODO Game discussion form -> including comments with their users, and accompanying time stamps