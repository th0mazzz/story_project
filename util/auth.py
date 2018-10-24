from flask import Flask
import sqlite3

def checkInfo(user,pswd):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    #Looks for the password of the inputted user
    for i in c.execute("SELECT pass FROM userInfo WHERE username = ?",(user,)):
         #If user is found and passwords match
        if i[0] == pswd: return "Login Successful"
         #If passwords don't match
        else: 
            db.close()
            return "Incorrect Password"
    else:
        #If the user doesn't exist in the table
        db.close()
        return "User not found"

def createAcc(user,pswd,passConf):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    #checks if the username already exists
    for i in c.execute("SELECT username FROM userInfo WHERE username = ?",(user,)):
        db.close()
        return "Username already exists"
    else:
        #if password confirmation fails
        if pswd != passConf: 
            db.close()
            return "Passwords do not match"        
        #if password confirmation succeeds add the user to the database
        c.execute("INSERT INTO userInfo (username,pass) VALUES(?,?)",(user,pswd,))
        db.commit()
        db.close()
        return "Account creation successful"

print(createAcc("abc","123","123")) #expect account creation successful

