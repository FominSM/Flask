from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
  full_name = StringField('Full Name', validators=[DataRequired()])
  e_mail = StringField('e-Mail', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
  confirmation_password = PasswordField('Password again', validators=[DataRequired(), Length(min=8), EqualTo('password')])
  date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
  check_box = BooleanField('Terms of use', validators=[DataRequired()])
