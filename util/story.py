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
        return "Successfully created story"
    db.commit()

print(createStory("First Story", "Bob", "I like trains"))
        
