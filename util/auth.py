from flask import Flask
import sqlite3

db = sqlite3.connect("info")

c = db.cursor()
