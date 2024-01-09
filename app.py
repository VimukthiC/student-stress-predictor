from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/home")
def home():
  return render_template('home.html')


@app.route("/signup")
def signup():
  return render_template('signup.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
