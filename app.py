#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from util import auth, story
from flask import Flask, request, render_template, session, url_for, redirect, flash
app = Flask(__name__) #Create instance of class Flask

app.secret_key = 'supersecure'


@app.route("/") #Assign fxn to route
def index():
    #if the user is logged in redirect them to their profile page
    if 'user' in session:
        return redirect('/profile')
    #if not, load the login page
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/auth",methods = ['POST'])
def authenticate():
    loginStatus = ''
    #if the user isn't logged in, redirect them to the login page
    if not('user' in request.form.keys()):
        redirect('/')
    #checks the user's login info
    if "pass2" in request.form.keys():
        loginStatus =  auth.createAcc(request.form['user'],request.form['pass1'],request.form['pass2'])
    else: loginStatus = auth.checkInfo(request.form["user"],request.form["pass"])
    #if the user successsfully logs in or creates an acount, redirect them to their profile page
    if loginStatus in ["Account creation successful","Login Successful"]:
        session['user'] = request.form['user']
        return redirect('/profile')
    else:
        flash(loginStatus)
        #Redirects to previous page or root if there is none
        return redirect(request.referrer or '/')

    
@app.route('/profile')
def profile():
    #if the user isn't logged in, redirect them to the login page
    if 'user' not in session.keys():
        redirect('/')
    #otherwise, load the user's profile page
    return render_template('profile.html',user = session['user'], stories = story.getStories(session['user']))


@app.route('/logout')
def logout():
    #if the user is logged in, log them out and redirect to the login page
    if 'user' in session:
        session.pop('user')
    return redirect('/')


@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route("/forbidden")
def forbidden():
    return "Forbidden"


if __name__ == "__main__":
    app.debug = True
    app.run()
