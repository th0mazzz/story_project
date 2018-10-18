from flask import Flask
import sqlite3

db = sqlite3.connect("../data/info.db")

c = db.cursor()

def checkInfo(user,pswd):
    #Looks for the password of the inputted user
    for i in c.execute("SELECT pass FROM userInfo WHERE username = ?",(user,)):
        if i[0] == pswd: return "Login Successful" #If user is found and passwords match
        else: return "Incorrect Password" #If passwords don't match
    else:
        return "User not found" #If the user doesn't exist in the table

def createAcc(user,pswd,passConf):
    for i in c.execute("SELECT username FROM userInfo WHERE username = ?",(user,)):
        return "Username already exists"
    else:
        if pswd != passConf: return "Passwords do not match"
        c.execute("INSERT INTO userInfo (username,pass) VALUES(?,?)",(user,pswd,))
        return "Account creation successful"
    db.commit()
