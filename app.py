from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

Users = [{
    'username': 'user1',
    'email': 'user1@gmail.com',
    'password': '12345'
}, {
    'username': 'user2',
    'email': 'user2@gmail.com',
    'password': '12345'
}]


@app.route("/home")
def home():
  return render_template('home.html')


@app.route("/signup")
def signup():
  return render_template('signup.html', users=Users)


@app.route("/login")
def login():
  return render_template('login.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
