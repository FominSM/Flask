from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  full_name = db.Column(db.String(80), nullable=False)
  e_mail = db.Column(db.String(80), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)
  date_birth = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'User("{self.full_name}", "{self.e_mail}")'
