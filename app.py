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

Review = db.Table(
        'Reviews',
        db.Model.metadata,
        db.Column('text', db.Unicode, nullable=False),
        db.Column('User_id', db.ForeignKey('Users.id'),primary_key=True),
        db.Column('Game_id', db.ForeignKey('Games.id'),primary_key=True),
        extend_existing=True
    )

ForumComment = db.Table(
        'ForumComments',
        db.Model.metadata,
        db.Column('content',db.LargeBinary, nullable=False),
        db.Column('timestamp',db.Date, nullable=False),
        db.Column('User_id', db.ForeignKey('Users.id'),primary_key=True),
        db.Column('Game_id', db.ForeignKey('Games.id'),primary_key=True),
        extend_existing=True
    )

# Create a database model for Users
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute
    revGames = db.relationship('Game', secondary=Review, back_populates='revUsers')
    comGames = db.relationship('Game', secondary=ForumComment, back_populates='comUsers')

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
    revUsers = db.relationship('User', secondary=Review, back_populates='revGames')
    comUsers = db.relationship('User', secondary=ForumComment, back_populates='comGames')


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
        
        
        # TODO complete tasks below
        # call api and create games
        # create comments
        # create reviews

        db.session.add_all((owner, u1, u2, u3, u4))
        db.session.commit()

# TODO sample q's

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