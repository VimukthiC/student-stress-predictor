from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,ValidationError
import bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'WTF_CSRF_SECRET_KEY'

mysql = MySQL(app)

class RegistrationForm(FlaskForm):
    name = StringField("User Name",validators=[DataRequired()])
    email = StringField("Email Address",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Sign In")

    def validate_email(self,field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s",(field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError("Email already taken")



@app.route("/", methods=["POST","GET"])
def home():
   return render_template('home.html')
    

@app.route("/signup", methods=["POST","GET"])
def signup():
    return render_template("signup.html")


@app.route("/login",  methods = ['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return "hello world"


if __name__ == "__main__":
  app.run(debug=True)
