from flask import Flask
import sqlite3

db = sqlite3.connect("../data/info.db")

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
    for i in c.execute("SELECT name FROM stories WHERE name = ?", (title,)):
        for z in c.execute("SELECT name FROM stories WHERE name = ? AND username != ?", (title,username,)):
            c.execute("INSERT INTO stories (name,username,contrib) VALUES(?,?,?)",(title,username,newLine,))
            db.commit()
            return "Successfully added to story"
        return "You have already added to this story"
    else:
        return "Cannot find given story"            
    
print(createStory("First Story", "Bob", "I like trains"))  #expect succesfully added
print(createStory("First Story", "Joe", "I like trains too"))  #expect title already exists
print(editStory("First Story", "Bob", "Did I mention that I like trains?")) #expect You have already added 
print(editStory("First Story", "Joe", "I like dogs")) #expect successfully added
print(editStory("Second Story", "Fred", "Is this right?")) #expect cannot find given story
