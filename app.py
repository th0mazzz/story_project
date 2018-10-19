#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from util import auth
from flask import Flask, request, render_template, session, url_for, redirect, flash
app = Flask(__name__) #Create instance of class Flask


@app.route("/") #Assign fxn to route
def index():
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/auth",methods = ['POST'])
def authenticate():
    if "pass2" in request.form.keys():
        return auth.createAcc(request.form['user'],request.form['pass1'],request.form['pass2'])
    return auth.checkInfo(request.form["user"],request.form["pass"])

@app.route("/forbidden")
def forbidden():
    return "Forbidden"

if __name__ == "__main__":
    app.debug = True
    app.run()
