from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class AddBook(FlaskForm):
    title = StringField('Book Title',
                         validators=[DataRequired(message="Enter title please!")])
    author = StringField('Author',
                          validators=[DataRequired(message="Enter author please!")])
    isbn = StringField('ISBN number')
    year = StringField('Publication Year')
    rating = StringField('Rating (1-5)')
    review = StringField('Review')
    submit = SubmitField('Add Book')

class FindBook(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    submit = SubmitField('Find Book')

class AddReview(FlaskForm):
    rating = IntegerField('Rating')
    review = StringField('Review',
                        validators=[DataRequired('Enter review please!')])
    submit = SubmitField('Add review')

class SignupForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),
                        Length(min=6),
                        Email(message='Please enter a valid email')])
    password = PasswordField('Password',
                           validators=
                            [DataRequired(),
                             Length(min=6,
                                    message='Please select a stronger password.')])
    confirm = PasswordField('Confirm your Password',
                           validators=[DataRequired(),
                                       EqualTo('password',
                                                message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class GoogleLogin(FlaskForm):
    submit = SubmitField('Login using Google!')
