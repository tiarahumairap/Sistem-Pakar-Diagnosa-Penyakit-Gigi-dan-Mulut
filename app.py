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


@app.route('/indexadm') #index
def indexadm():
    return render_template('indexadm.html')

@app.route('/gejala') #index
def gejala():
    return render_template('gejaladm.html')

@app.route('/addgejala')
def addgejala():
    return render_template('addgejala.html')

@app.route('/updategejala')
def updategejala():
    return render_template('updategejala.html')

@app.route('/penyakit')
def penyakit():
    return render_template('penyakitadm.html')

@app.route('/addpenyakit')
def addpenyakit():
    return render_template('addpenyakit.html')

@app.route('/updatepenyakit')
def updatepenyakit():
    return render_template('updatepenyakit.html')

@app.route('/basis')
def basis():
    return render_template('basisadm.html')

@app.route('/addbasis')
def addbasis():
    return render_template('addbasis.html')

@app.route('/detailbasis')
def detailbasis():
    return render_template('detailbasis.html')


if __name__ == '__main__':
    app.run (debug = True)