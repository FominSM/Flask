from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from models import db, User
from logging import getLogger as Logger
from registration_form import RegistrationForm
import re
import os
import hashlib



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'
db.init_app(app)
csrf = CSRFProtect(app)


@app.cli.command("init-db")
def init_db():
  db.create_all()
  print('OK')


@app.get('/')
def home():
  context = {'users': User.query.all()}
  return render_template('home.html', **context)

@app.get('/hello/<name>')
def hello(name):
  return render_template('hello.html', name=name)


@app.route('/register/', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()

  if request.method == 'POST' and form.validate():
    user = User(
      full_name=form.full_name.data,
      e_mail=form.e_mail.data,
      password=__password_hash(form.password.data),
      date_birth=form.date_of_birth.data
    )

    if User.query.filter_by(e_mail=form.e_mail.data).first():
      response = make_response(redirect(url_for('register')))
      flash('A user with this email already exists !!!', 'error')
      return response
    elif not __password_validate(form.password.data):
      response = make_response(redirect(url_for('register')))
      flash('The password field must contain at least 8 characters, including at least 1 letter and 1 number !!!', 'error')
      return response

    db.session.add(user)
    db.session.commit()
    response = make_response(redirect(url_for('hello', name=user.full_name)))
    flash('SignUp was successfully!', 'success')
    return response
   
  else:
    return render_template('register.html', form=form)
  

def __password_validate(password):
  '''Password validity check, minimum 8 characters, 1 capital letter, 1 lower case letter, 1 number'''

  pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$') 
  return bool(pattern_password.match(password))

def __password_hash(password):
  '''Hashing passwords with pbkdf2_hmac'''

  salt = os.urandom(16)
  key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
  return key

 

@app.errorhandler(404)
def page_not_found(e):
  context = {
    'title': 'Page not found =(',
    'url': request.referrer,
  }
  return render_template('404.html', **context), 404
