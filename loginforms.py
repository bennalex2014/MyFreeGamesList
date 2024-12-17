from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, SubmitField, EmailField, SelectField, IntegerField, StringField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange

# TODO change to match DB
class RegisterForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    username = StringField("Username: ", validators=[InputRequired(), Length(min=3, max=24)])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    confirm_password = PasswordField("Confirm Password: ", 
        validators=[EqualTo('password')])
    submit = SubmitField("Register")

# TODO change to match DB
class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[InputRequired(), Email()])
    password = PasswordField("Password: ", 
        validators=[InputRequired(), Length(min=8, max=256)])
    submit = SubmitField("Login")
    

# TODO change to match DB
class ReviewForm(FlaskForm):
    game = SelectField("Game: ", choices=[])
    score = IntegerField("Rating: ", validators=[InputRequired(), NumberRange(1, 10)])
    review = StringField("Review: ", validators=[InputRequired()])
    submit = SubmitField("Add Review")

# TODO change to match DB
class CommentForm(FlaskForm):
    comment = StringField("Comment: ", validators=[InputRequired(), Length(3, 255)])
    submit = SubmitField("Add Comment")