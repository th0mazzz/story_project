from flask import Flask
import sqlite3

db = sqlite3.connect("data/info.db",check_same_thread=False)

c = db.cursor()

def createStory(title,username,firstLine):
    #checks if title is unique
    for i in c.execute("SELECT name FROM stories WHERE name = ?", (title,)):
        return "Title already exists"
    else:
        #inserts given information into the table
        c.execute("INSERT INTO stories (name,username,contrib) VALUES(?,?,?)",(title,username,firstLine,))
        db.commit()
        return "Successfully created story"

def editStory(title,username,newLine):
    #checks if the user already made a contribution
    for i in c.execute("SELECT name FROM stories WHERE name = ? AND username = ?",(title,username,)):
        return "You have already contributed"
    else:
        #inserts given information into the table
        for z in c.execute("SELECT name FROM stories WHERE name = ?", (title,)):
            c.execute("INSERT INTO stories (name,username,contrib) VALUES(?,?,?)",(title,username,newLine,))
            db.commit()
            return "Successfully added to story"
        return "Story does not exist"


def getStories(username):
    #selects all the stories the user has contributed to
    c.execute("SELECT name FROM stories WHERE username = ?", (username,))
    rows = c.fetchall()
    print(rows)
    return(rows)

getStories("Bob")
#diagnostic print statements
print(createStory("First Story", "Bob", "I like trains"))  #expect succesfully added
print(createStory("First Story", "Joe", "I like trains too"))  #expect title already exists
print(editStory("First Story", "Bob", "Did I mention that I like trains?")) #expect You have already added
print(editStory("First Story", "Joe", "I like dogs")) #expect successfully added
print(editStory("Second Story", "Fred", "Is this right?")) #expect cannot find given story
print(createStory("Bob's Story", "abc", "wassup"))
