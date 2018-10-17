#Team SKAR - Sophia Xia, Kevin Lin, Aaron Li, Ricky Lin

from flask import Flask
app = Flask(__name__) #Create instance of class Flask

@app.route("/") #Assign fxn to route
def hello_world():
    return "No hablo queso!"

@app.route("/forbidden")
def forbidden():
    return "Forbidden"

if __name__ == "__main__":
    app.debug = True
    app.run()
