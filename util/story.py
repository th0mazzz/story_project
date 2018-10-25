from flask import Flask
import sqlite3

def createStory(title,username,firstLine):
    #checks if title is unique
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    for i in c.execute("SELECT name FROM stories WHERE name = ?", (title,)):
        db.close()
        return "Title already exists"
    else:
        #inserts given information into the table
        c.execute("INSERT INTO stories (name,username,contrib) VALUES(?,?,?)",(title,username,contentParser(firstLine),))
        db.commit()
        db.close()
        return "Successfully created story"

def editStory(title,username,newLine):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    #checks if the user already made a contribution
    for i in c.execute("SELECT name FROM stories WHERE name = ? AND username = ?",(title,username,)):
        db.close()
        return "You have already contributed"
    else:
        #inserts given information into the table
        for z in c.execute("SELECT name FROM stories WHERE name = ?", (title,)):
            c.execute("INSERT INTO stories (name,username,contrib) VALUES(?,?,?)",(title,username,contentParser(newLine),))
            db.commit()
            db.close()
            return "Successfully added to story"
        db.close()
        return "Story does not exist"

def contentParser(content):
    output = ""
    i = 0
    italics = False
    bold = False
    underline = False
    while i < len(content):
        if content[i] != '<':
            if content[i:i+5] == '[img ':
                bracketcount = 0
                subt = ''
                success = False
                for j in range(i+5,len(content)):
                    if content[j] == '[':
                        bracketcount += 1
                    elif content[j] == ']':
                        bracketcount -= 1
                        if bracketcount < 0:
                            success = True
                            break
                    else:
                        subt+= content[j]
                if success:
                    output += '<img src = "' + subt + '">'
                    i += len(subt) + 6
                    continue
                output += '[img '
                i += 5
                continue
            elif content[i:i+3] == '[i]':
                if italics:
                    output += '</i>'
                    italics = False
                else:
                    output += '<i>'
                    italics = True
                i += 3
                continue
            elif content[i:i+3] == '[b]':
                if bold:
                    output += '</b>'
                    bold = False
                else:
                    output += '<b>'
                    bold = True
                i += 3
                continue
            elif content[i:i+3] == '[u]':
                if underline:
                    output += '</u>'
                    underline = False
                else:
                    output += '<u>'
                    underline = True
                i += 3
                continue
            elif content[i:i+1] == '\n':
                output += '<br>'
            output += content[i]
        else: output += '&lt'
        i += 1
    if italics:
        output += '</i>'
    if bold:
        output += '</b>'
    if underline:
        output += '</u>'
    return output

def getAll():
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    c.execute("SELECT name FROM stories")
    everything = c.fetchall()
    output = set()
    for i in everything:
        output.add(i[0])
    #print(output)
    db.close()
    return(output)

def getStories(username):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    #selects all the stories the user has contributed to
    c.execute("SELECT name FROM stories WHERE username = ?", (username,))
    rows = c.fetchall()
    output = set()
    for i in rows:
        output.add(i[0])
    #print(output)
    db.close()
    return(output)

def getUndiscovered(username):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    output = getAll() - getStories(username)
    db.close()
    return output
    #print(output)

def getLast(storyname):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    #Selects latest entry of the story
    for i in c.execute("SELECT contrib FROM stories WHERE name = ? ORDER BY ROWID DESC LIMIT 1;",(storyname,)):
        #Return latest entry if found
        db.close()
        return [i[0]]
    else:
        #Returned if no entry found
        db.close()
        return ["Story does not exist"]

def getDiscoverDict(username):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    output = dict()
    undisList = getUndiscovered(username)
    for i in undisList:
        output[i] = getLast(i)[0]
    db.close()
    return output

def getFull(storyname):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    output = []
    for i in c.execute("SELECT contrib FROM stories WHERE name = ? ORDER BY ROWID;",(storyname,)):
        output.append(i[0]) #Adds all entries of a story in order of insertion to an output string
    if len(output) == 0:
        db.close()
        return ['Story does not exist'] #Returned if no story found
    db.close()
    return output

#gets the creator of the story
def getAuthor(storyname):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    for i in c.execute("SELECT username FROM stories WHERE name = ? ORDER BY ROWID LIMIT 1;",(storyname,)):
        #Return latest entry if found
        db.close()
        return i[0]
    else:
        #Returned if no entry found
        db.close()
        return "Story does not exist"

def getSpecificAuthor(storyname, content):
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    c.execute("SELECT username FROM stories WHERE name = ? AND contrib = ?", (storyname, content,))
    contributor = c.fetchone()
    db.close()
    return contributor[0]

#diagnostic print statements
print(getAll())
print(getStories("Bob"))
print(getUndiscovered("Bob"))
print(createStory("First Story", "Bob", "I like trains"))  #expect succesfully added
print(createStory("First Story", "Joe", "I like trains too"))  #expect title already exists
print(editStory("First Story", "Bob", "Did I mention that I like trains?")) #expect You have already added
print(editStory("First Story", "Joe", "I like dogs")) #expect successfully added
print(editStory("Second Story", "Fred", "Is this right?")) #expect cannot find given story
print(createStory("Bob's Story", "abc", "wassup"))
