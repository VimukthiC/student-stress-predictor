from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
  return render_template('home.html')


@app.route("/signIn")
def signIn():
  return render_template('sign_in.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
