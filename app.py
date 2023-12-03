from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import initialize_database, create_database, id_user, get_database_cursor, db, kode_gejala

app = Flask(__name__)
app.secret_key = 'ara20102196ara'

db = initialize_database()
create_database()
cursor = get_database_cursor()

@app.route('/addu', methods=['POST'])
def addu():
    name = request.form['name']
    usia = request.form['age']
    jk = request.form['jk']
    next_id = id_user()

    cursor.execute("INSERT INTO users (id, name, age, jk) VALUES (%s, %s, %s, %s)", (next_id, name, usia, jk))
    db.commit()

    session['uname'] = name

    return redirect(url_for('dtdiag'))

@app.route('/dtdiag')
def dtdiag():
    # Ambil nama dari sesi Flask
    user_name = session.get('uname')

    cursor.execute("SELECT * FROM symptoms")
    symptoms = cursor.fetchall()
    db.commit()
    print(symptoms)


    return render_template('indexdata.html', uname=user_name, symptoms=symptoms)

@app.route('/submit_diagnosis', methods=['POST'])
def submit_diagnosis():
    selected_symptom_codes = request.form.getlist('gejala')
    print("Kode Gejala yang dicentang:", selected_symptom_codes)

    # Ambil gejala yang sesuai dengan kode gejala yang dicentang
    selected_symptoms = []
    for symptom_code in selected_symptom_codes:
        cursor.execute("SELECT gejala FROM symptoms WHERE kode_gejala = %s", (symptom_code,))
        result = cursor.fetchone()
        if result:
            selected_symptoms.append(result[0])

    # Gabungkan nilai gejala menjadi string (Anda dapat menggunakan separator yang sesuai)
    pilihan_gejala = ",".join(selected_symptoms)

    # Simpan nilai ke dalam database
    cursor.execute("UPDATE users SET pilihan_gejala = %s WHERE name = %s",
                   (pilihan_gejala, session['uname']))
    db.commit()

    return redirect(url_for('result', message='Data gejala telah disimpan ke dalam database!'))

@app.route("/result")
def result():
    return render_template('indexresult.html')

@app.route("/")
def home():
    return render_template('indexweb.html')

@app.route("/login")
def login():
    return render_template('loginweb.html')

@app.route("/indiag")
def indiag():
    return render_template('indexinput.html')

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