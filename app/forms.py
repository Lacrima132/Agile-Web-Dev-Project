from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileAllowed, FileRequired

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password1', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    keyword = StringField('Keyword')
    submit = SubmitField('Search')  

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

class DiscussionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    desc = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileEditForm(FlaskForm):
    username = StringField('Username')
    bio = StringField('Bio')
    image = FileField('Profile Image')
    submit = SubmitField('Submit')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Submit')

class SellForm(FlaskForm):
    weapon_title = StringField('Weapon Title', validators=[DataRequired()])
    weapon_price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    weapon_description = TextAreaField('Weapon Description', validators=[DataRequired()])
    weapon_image = FileField('Upload Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')

def validate_integer(form, field):
    try:
        int(field.data)
    except ValueError:
        raise ValidationError("Price must be an integer.")

class BountyForm(FlaskForm):
    target = StringField('Target', validators=[
        DataRequired(), 
        Length(min=1, max=100, message="Target name must be between 1 and 100 characters")
    ])
    price = StringField('Price', validators=[
        DataRequired(),
        validate_integer
    ])
    tinfo = TextAreaField('Target Information', validators=[
        DataRequired(), 
        Length(min=1, message="Target information must not be empty")
    ])
    weapon_image = FileField('Upload Image', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    category_menu = SelectField('Dead or Alive?', choices=[
        ('Dead', 'Dead'),
        ('Alive', 'Alive'),
        ('Either', 'Either')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')