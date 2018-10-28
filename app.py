#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from util import auth, story
from flask import Flask, request, render_template, session, url_for, redirect, flash
import os

app = Flask(__name__) #Create instance of class Flask

app.secret_key = os.urandom(32)

@app.route("/") #Assign fxn to route
def index():
    '''This function redirects the user to their profile page if they are logged in.
       If they aren't, it will render the login page
       where the users will be prompted to enter their username and password.
       When users enter and submit the information,
       they will be redirected to the authentication page.'''
    #if the user is logged in redirect them to their profile page
    if 'user' in session:
        return redirect('/profile')
    #if not, load the login page
    return render_template("index.html")


@app.route("/create")
def create():
    '''This function redirects the user to their profile page if they are logged in.
       If they aren't, it will render the account creator page
       where they will be prompted to enter their desired username and password
       as well as confirm their password.
       Once the user sumbits their information, they will be redirected to their profile page.
       Users can also click the login link which brings them back to the login page.'''
    if 'user' in session:
        return redirect('/profile')
    return render_template("create.html")


@app.route("/auth",methods = ['POST'])
def authenticate():
    '''This function redirects users who got to the the authenticate page without entering a form to the login page.
       If they did enter a form, it will check if the username and password are in the database.
       If they are, it will redirect them to their profile page and flash a message indicating a successful login.
       If they aren't, it will redirect them to the login page and flash a message indicating the issue.
       Whether the username or the password was incorrect.
       If they were both incorrect, the message will only indicate an issue with the username.'''
    loginStatus = ''
    #if the user got here without entering a form, redirect them to the index
    if not('user' in request.form.keys()):
        return redirect('/')
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
    '''This function redirects the user to the login page if they aren't logged in.
       If they are, it will render their profile page.
       On their profile page, there is a list of links to stories they have contributed to.
       Users can also click a link to discover new stories or a link to create a new story.
       They can also click the logout link.'''
    #if the user isn't logged in, redirect them to the login page
    if not('user' in session):
        return redirect('/')
    #otherwise, load the user's profile page
    storiesList = story.getStories(session['user'])
    if len(storiesList) == 0:
        storiesList = ['You have not contributed to any stories!']
    return render_template('profile.html',user = session['user'], stories = storiesList)

@app.route('/logout')
def logout():
    '''This function will logout the user if they are logged in.
       Then it will redirect the user to the login page.'''
    #if the user is logged in, log them out and redirect to the login page
    if 'user' in session:
        session.pop('user')
        flash('Sucessfully Logged Out')
    return redirect('/')

@app.route('/discover')
def discover():
    '''This function redirects the user to the login page if they aren't logged in.
       If the user is logged in, it will render the discover page.
       The discover page lists links to stories the user has not contributed to
       as well as show the last submission, last submissions author, and creator of the story.
       The user can click a link to return to their profile page.'''
    if not('user' in session):
        return redirect('/')
    def getA(storyname):
        return story.getAuthor(storyname)
    def getSA(storyname, content):
        return story.getSpecificAuthor(storyname, content)
    storiesList = story.getDiscoverDict(session['user'])
    if len(story.getAll()) == 0:
        flash('There are no stories, please contribute')
        return redirect('/contribute')
    if len(storiesList) == 0:
        storiesList = dict()
        storiesList['WOW you\'ve contributed to all stories available!'] = ''
        #return render_template('discover.html', keys = storiesList.keys(), dct = storiesList, ga = getA)
    return render_template('discover.html', keys = storiesList.keys(), dct = storiesList, ga = getA, gsa = getSA)

@app.route('/edit')
def edit():
    '''This function will redirect the user to the login page if they aren't logged in.
       If they are logged in and the story is valid, it will render the edit page.
       The User will be able to add onto the existing story while viewing the previous submission.
       The content will be added through the editchanges route.
       If the story doesn't exist, the user will be redirected to their profile page.
       Users can also choose to return to discover or logout with the links at the bottom of the page.'''
    storyname = ''
    try:
        storyname = request.args['story']
    except:
        return redirect("/discover")
    if 'user' in session:
        if not storyname in story.getStories(session['user']):
            storycontent = story.getLast(storyname)[0]
        else: return redirect('/profile')
    else:
        return redirect('/')
    if not storyname in story.getAll():
        return redirect("/discover")
    return render_template('edit.html', story_title = storyname, story = storycontent, contributor = story.getAuthor(storyname))

@app.route('/editchanges', methods = ["POST","GET"])
def editChanges():
    '''This function redirects the user to the login page if they aren't logged in
       or if a story name wasn't inputted.
       Otherwise, it will add the story content into the database
       and redirect the user to their profile page.
       '''
    if not('story' in request.args): return redirect('/')
    if not('user' in session):
        return redirect('/')
    storyname = request.args['story']
    storycontent = request.form['story_content']
    story.editStory(storyname, session['user'], storycontent)
    return redirect("/profile")

@app.route("/contribute", methods = ["POST", "GET"])
def contribute():
    '''This function redirects the user to the login page if they aren't logged in.
       otherwise, it checks if you already submitted a contribution and posted something. If you posted, it will add the change to the database and redirect you to your profile. Else, it will return the same page
    '''
    if not('user' in session):
        return redirect('/')
    method = request.method
    if method == "POST":
        storyname = request.form['story_title']
        story_content = request.form['story_content']
        story.createStory(storyname, session['user'], story_content)
        return redirect("/profile")
    else:
        return render_template("contribute.html")

@app.route("/forbidden")
def forbidden():
    '''This function shows Forbidden on the page'''
    return "Forbidden"

@app.route('/view')
def view():
    '''This function redirects the user to the login page if they aren't logged in.
       Otherwise, it will try to get the storyname and if it fails, it will redirect to the profile page.
       If it succeeds, it will check to see if the user has contributed to it before.
       If the user has, it will show the full story and if not it will only show the last submission.
       It will also display the names of all the contributors.
       If the storyname isn't in the database, it redirects the user to their profile page
       User can go to their profile or logout with the links at the bottom of the page.'''
    if not('user' in session):
        return redirect('/')
    def getSA(storyname, content):
        return story.getSpecificAuthor(storyname, content)
    storyname = ''
    try:
        storyname = request.args['story']
    except:
        return redirect("/profile")
    storycontent = ''
    if 'user' in session:
        if storyname in story.getStories(session['user']):
            storycontent = story.getFull(storyname)
    else:
        storycontent = story.getLast(storyname)
    if not storyname in story.getAll():
        return redirect("profile")
    return render_template('view.html', story = storyname, content = storycontent, gsa = getSA)

if __name__ == "__main__":
    app.debug = True
    app.run()
