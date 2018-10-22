#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from util import auth, story
from flask import Flask, request, render_template, session, url_for, redirect, flash
app = Flask(__name__) #Create instance of class Flask

app.secret_key = 'supersecure'

@app.route("/") #Assign fxn to route
def index():
    if 'user' in session.keys():
        return redirect('/profile')
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/auth",methods = ['POST'])
def authenticate():
    loginStatus = ''
    if not('user' in request.form.keys()):
        redirect('/')
    if "pass2" in request.form.keys():
        loginStatus =  auth.createAcc(request.form['user'],request.form['pass1'],request.form['pass2'])
    else: loginStatus = auth.checkInfo(request.form["user"],request.form["pass"])
    if loginStatus in ["Account creation successful","Login Successful"]:
        session['user'] = request.form['user']
        return redirect('/profile')
    else:
        flash(loginStatus)
        #Redirects to previous page or root if there is none
        redirect(request.referrer or '/')

@app.route('/profile')
def profile():
    return render_template('profile.html',user = session['user'], stories = story.getStories(session['user']))

@app.route("/forbidden")
def forbidden():
    return "Forbidden"

if __name__ == "__main__":
    app.debug = True
    app.run()
