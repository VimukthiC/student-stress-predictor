from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,ValidationError
import bcrypt
from flask_mysqldb import MySQL
import pickle
import numpy as np

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'b6mfqiatycs4vihuictl-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uu5atsbg5gs51adw'
app.config['MYSQL_PASSWORD'] = 'XGPAtmZRkmhrJD7N18mi'
app.config['MYSQL_DB'] = 'b6mfqiatycs4vihuictl'
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
    sleep_quality = StringField("Rate your sleep quality?",validators=[DataRequired()])
    suffer_headaches = StringField("How many times a week do you suffer headaches?",validators=[DataRequired()])
    academic_performance = StringField("How would you rate you academic performance?",validators=[DataRequired()])
    study_load = StringField("How would you rate your study load?",validators=[DataRequired()])
    extracurricular_activities = StringField("How many times a week you practice extracurricular activities?",validators=[DataRequired()])
    submit = SubmitField("Predict")

model = pickle.load(open('ml_model/ss_model.pkl', 'rb'))


@app.route("/", methods=["GET"])
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


@app.route("/login",  methods= ["POST","GET"])
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

@app.route('/dashboard', methods = ["POST","GET"])
def dashboard():
    try:

        output = None
        form = PredictorForm()
        if form.validate_on_submit():
            sleep_quality = form.sleep_quality.data
            suffer_headaches = form.suffer_headaches.data
            academic_performance = form.academic_performance.data
            study_load = form.study_load.data
            extracurricular_activities = form.extracurricular_activities.data

            features = np.array([[sleep_quality, suffer_headaches, academic_performance, study_load, extracurricular_activities]])
            prediction = model.predict(features)
            output = round(prediction[0], 1)

            if (output>= 0 and output <= 1.3):
                flash("Low Stress : Students in this category experience minimal stress. They may feel calm, relaxed, and in control of their academic and personal responsibilities. Stress level : %s" %output)
            elif (output>1.3 and output<=2.3):
                flash("Mild Stress : Students with mild stress may encounter occasional challenges but generally cope well. They can manage their workload and handle stressors effectively. Stress level : %s" %output)
            elif (output>2.3 and output<=3.3):
                flash("Moderate Stress : This level indicates a moderate amount of stress. Students may face increased pressure, multiple demands, or some difficulties in managing their academic and personal commitments. Stress level : %s" %output)
            elif (output>3.3 and output<=4.3):
                flash("High Stress : Students experiencing high stress levels may find it challenging to cope with the demands of their studies and life. Stressors may be impacting their overall well-being. Stress level : %s" %output)
            else :
                flash("Very High Stress : This level represents an extreme amount of stress. Students in this category may be overwhelmed, struggling to manage their workload, and may need additional support to address their stressors. Stress level : %s" %output)
            
        return render_template("dashboard.html",form = form,output = output)

    except Exception as e:
        print(e)
        return render_template("dashboard.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logout successfully")
    return redirect(url_for('login'))   

    

    
if __name__ == "__main__":
  app.run(debug=True)
