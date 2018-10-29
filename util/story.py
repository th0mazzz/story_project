from flask import Flask
import sqlite3

def createStory(title,username,firstLine):

    '''This function takes in 3 parameters (title, username, firstLine).
       It checks the database to see if the title already exists.
       If it does, it returns, "Title already exists".
       Otherwise it will insert the information into the database
       and return "Successfully created story".'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    #checks if title is unique
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
    
    '''This function takes in 3 parameters (title, username, firstLine).
       It checks to see if the title username pair matches any entries in the database.
       If it does, the function returns "You have already contributed".
       Otherwise, it will add the information to the database and return "Successfully added to story".
       Unless the story isn't found in the database,
       which will make the function return "Story does not exist".'''
    
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
    
    '''This function takes in one parameter (content).
       It parses through content for tags:
       replaces the following with html formatting tags
          [img link_to_image] -> inserts image
          [i] -> italicizes words
          [b] -> bolds words
          [u] -> underlines words
          \n -> new line
        to prevent use of html formatting
       < -> &lt
       it returns the edited version of content.
       '''
    
    output = ""
    i = 0
    italics = False
    bold = False
    underline = False
    while i < len(content):
        if content[i] != '<':
            #If a start of an image tag is recognized
            if content[i:i+5] == '[img ':
                bracketcount = 0 #Keeps track of bracket balancing
                subt = ''
                success = False
                for j in range(i+5,len(content)):
                    if content[j] == '[':
                        bracketcount += 1
                    elif content[j] == ']':
                        bracketcount -= 1
                        if bracketcount < 0: #Ends the tag if brackets are balanced
                            success = True
                            break
                    else:
                        subt+= content[j] #Inserts characters in a link
                if success:
                    output += '<img src = "' + subt + '">' #Converts tag with link into HTML
                    i += len(subt) + 6 #Moves i to account for added characters
                    continue
                #If not successful (no ending brackets) add [img as part of the output
                output += '[img '
                i += 5
                continue
            elif content[i:i+3] == '[i]': #If an italics tag is recognized
                #Check if italics are on, either put an ending or beginning of italics, and toggle the boolean
                if italics:
                    output += '</i>'
                    italics = False
                else:
                    output += '<i>'
                    italics = True
                i += 3
                continue
            elif content[i:i+3] == '[b]': #If an bold tag is recognized
                #Check if bolding is on, either put an ending or beginning of bolding, and toggle the boolean
                if bold:
                    output += '</b>'
                    bold = False
                else:
                    output += '<b>'
                    bold = True
                i += 3
                continue
            elif content[i:i+3] == '[u]': #If an underline tag is recognized
                #Check if underlining is on, either put an ending or beginning of underlining, and toggle the boolean
                if underline:
                    output += '</u>'
                    underline = False
                else:
                    output += '<u>'
                    underline = True
                i += 3
                continue
            elif content[i:i+1] == '\n': #Adds a <br> whenever there's a new line since HTML doesn't recognize that
                output += '<br>'
            output += content[i]
        else: output += '&lt' #If someone's trying to be sneaky and insert html, replace < with &lt
        i += 1
    #Puts ending tags for formatting so the contribution doesn't affect the text on the page after it
    if italics:
        output += '</i>'
    if bold:
        output += '</b>'
    if underline:
        output += '</u>'
    return output #Returns edited contribution

def getAll():
    
    '''This function returns a list of all the story names from the database'''
    
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
    
    '''This function takes in one parameter(username).
       It returns a list of unique story names associated with the username from searching the database.'''
    
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
    
    '''This function takes in one parameter(username).
       It returns a list of unique story names unassociated with the username from searching the database.'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    output = getAll() - getStories(username)
    db.close()
    return output
    #print(output)

def getLast(storyname):
    
    '''This function takes in one parameter(storyname).
       It returns the latest content/text associated with the storyname.'''
    
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
    
    '''This function takes in one parameter(username).
       It returns a dictionary where
       the keys are the storynames of the stories the user is associated with the in database.
       The values are the latest content associated with their keys, which are the storynames.'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    output = dict()
    undisList = getUndiscovered(username)
    
    for i in undisList:
        output[i] = getLast(i)[0]
    
    db.close()
    return output

def getFull(storyname):
    
    '''This function takes in one parameter(storyname).
       It searches the database for the storyname
       and returns a list of all the content associated with the storyname.
       If the story doesn't exist, it will just return "Story does not exist".'''
    
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
    
    '''This function takes in one parameter(storyname).
       It returns the creator/first contributor to the story
       after searching throught the database for the first username associated with the storyname.'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    for i in c.execute("SELECT username FROM stories WHERE name = ? ORDER BY ROWID LIMIT 1;",(storyname,)):
        #Return latest entry if found
        db.close()
        return i[0]
    
    else:
        #Returned if no entry found
        db.close()
        return "No author"
        #return "Story does not exist"

def getSpecificAuthor(storyname, content):
    
    '''This function takes in two parameters(storyname, content).
       It searches the database for the username associated with both the storyname and content.
       It returns that specific username.'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    c.execute("SELECT username FROM stories WHERE name = ? AND contrib = ?", (storyname, content,))
    contributor = c.fetchone()
    db.close()
    if contributor == None: return ''
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
