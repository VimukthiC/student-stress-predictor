from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Email,ValidationError
import bcrypt
from flask_mysqldb import MySQL
import pickle

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

class LoginForm(FlaskForm):
    email = StringField("Email Address",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")

class PredictorForm(FlaskForm):
    sleep = IntegerField("Rate your Sleep quality?",validators=[DataRequired()])
    headaches = IntegerField("How many times a week do you suffer headaches?",validators=[DataRequired()])
    academic = IntegerField("How would you rate you academic performance?",validators=[DataRequired()])
    study = IntegerField("How would you rate your study load?",validators=[DataRequired()])
    activities = IntegerField("How many times a week you practice extracurricular activities?",validators=[DataRequired()])
    submit = SubmitField("Predict")

    
        
def  prediction(list):
        fileName = 'ml_model/student_stress.pickle'
        with open(fileName, 'rb') as file:
            model = pickle.load(file)
        predict_value = model.predict([list])
        return predict_value

@app.route("/", methods=["POST","GET"])
def home():
   return render_template('home.html')
    

@app.route("/signup", methods=["POST","GET"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)",(name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))
    return render_template("signup.html" , form = form)


@app.route("/login",  methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s",(email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password.")
            return redirect(url_for('login'))

    return render_template("login.html", form = form)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    form = PredictorForm()
    if form.validate_on_submit():
        sleep = form.sleep.data
        headaches = form.headaches.data
        academic = form.academic.data
        study = form.study.data
        activities = form.activities.data

        feature_list = []
        feature_list.append(sleep)
        feature_list.append(headaches)
        feature_list.append(academic)
        feature_list.append(study)
        feature_list.append(activities)

        Predict = prediction(feature_list)
        print(Predict)

    return render_template("dashboard.html", form = form)


if __name__ == "__main__":
  app.run(debug=True)
