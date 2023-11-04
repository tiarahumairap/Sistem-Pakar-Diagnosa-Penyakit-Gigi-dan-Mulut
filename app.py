from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('indexweb.html')

@app.route("/login")
def login():
    return render_template('loginweb.html')

@app.route("/indiag")
def indiag():
    return render_template('indexinput.html')

@app.route("/dtdiag")
def dtdiag():
    return render_template('indexdata.html')



if __name__ == '__main__':
    app.run (debug = True)