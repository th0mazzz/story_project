import sqlite3

#open("../data/info.db","w").close() #Resets Database

db = sqlite3.connect("../data/info.db")

c = db.cursor()

#Setting up tables
c.execute("CREATE TABLE IF NOT EXISTS userInfo(id INTEGER PRIMARY KEY, username TEXT UNIQUE, pass TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS stories(name TEXT, username TEXT, contrib TEXT)")
