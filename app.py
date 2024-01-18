from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,ValidationError
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12677255'
app.config['MYSQL_PASSWORD'] = 'I8ZhUeXrEJ'
app.config['MYSQL_DB'] = 'sql12677255'
app.secret_key = 'WTF_CSRF_SECRET_KEY'

mysql = MySQL(app)


@app.route("/home")
def home():
  return render_template('home.html')


@app.route("/signup")
def signup():
  return render_template('signup.html')


@app.route("/login")
def login():
  return render_template('login.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
