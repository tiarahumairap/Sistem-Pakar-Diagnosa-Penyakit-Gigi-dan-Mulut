from flask import Flask, render_template, request, redirect, url_for, session
from database import initialize_database, create_database, id_user, get_database_cursor, db, insert_treatments, insert_preventions, insert_symptoms, insert_admins, check_admin_credentials

app = Flask(__name__)
app.secret_key = 'ara20102196ara'

db = initialize_database()
create_database()
cursor = get_database_cursor()
insert_treatments()
insert_preventions()
insert_symptoms()
insert_admins()

@app.route('/addu', methods=['POST'])
def addu():
    name = request.form['name']
    usia = request.form['age']
    jk = request.form['jk']
    next_id = id_user()

    cursor.execute("INSERT INTO users (user_id, name, age, jk) VALUES (%s, %s, %s, %s)", (next_id, name, usia, jk))
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
    try:
        cursor = get_database_cursor()

        selected_symptom_codes = request.form.getlist('gejala')
        print("Kode Gejala yang dicentang:", selected_symptom_codes)

        # Gabungkan nilai gejala menjadi string
        pilihan_kode_gejala = ",".join(selected_symptom_codes)

        # Dapatkan ID terakhir yang terdaftar dalam tabel users
        cursor.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            last_idu = result['user_id']

            # Perbarui data pada tabel users
            cursor.execute("UPDATE users SET pilihan_gejala = %s WHERE user_id = %s", (pilihan_kode_gejala, last_idu))
            db.commit()
        else:
            # Jika tidak ada baris dengan user_id tersebut, tambahkan baris baru
            next_id = id_user()
            cursor.execute("INSERT INTO users (user_id, pilihan_gejala) VALUES (%s, %s)", (next_id, pilihan_kode_gejala))
            db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()

    return redirect(url_for('indexresult.html', message='Data gejala telah disimpan ke dalam database!', pilihan_kode_gejala=pilihan_kode_gejala))

@app.route('/result')
def result():
    user_name = session.get('uname')

    # Dapatkan data pilihan_gejala dari tabel users
    cursor.execute("SELECT pilihan_gejala FROM users WHERE name = %s", (user_name,))
    result = cursor.fetchone()

    gejalas = []

    if result and result['pilihan_gejala']:
        pilihan_gejala = result['pilihan_gejala'].split(",")  # Pisahkan gejala menjadi list

        # Lakukan apa yang perlu Anda lakukan dengan pilihan_gejala, misalnya mendapatkan gejala
        for gejala_kode in pilihan_gejala:
            cursor.execute("SELECT gejala FROM symptoms WHERE kode_gejala = %s", (gejala_kode,))
            result_gejala = cursor.fetchone()

            if result_gejala and result_gejala['gejala']:
                gejala = result_gejala['gejala']
                gejalas.append(gejala)

    return render_template('indexresult.html', uname=user_name, gejalas=gejalas)

@app.route("/")
def home():
    return render_template('indexweb.html')

@app.route("/loginadm", methods=['GET', 'POST'])
def loginadm():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if check_admin_credentials(email, password):
            return redirect(url_for('indexadm'))
        else:
            return render_template('loginweb.html', error="Email atau password salah")

    else:
        return render_template('loginweb.html')

@app.route("/login")
def login():
    return render_template('loginweb.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/indiag")
def indiag():
    return render_template('indexinput.html')

@app.route('/indexadm') #index
def indexadm():
    cursor.execute("SELECT COUNT(*) as total_gejala FROM symptoms")
    result = cursor.fetchone()
    total_gejala = result['total_gejala']

    cursor.execute("SELECT COUNT(*) as total_pengobatan FROM treatments")
    result = cursor.fetchone()
    total_pengobatan = result['total_pengobatan']

    cursor.execute("SELECT COUNT(*) as total_pencegahan FROM preventions")
    result = cursor.fetchone()
    total_pencegahan = result['total_pencegahan']

    return render_template('indexadm.html', total_gejala=total_gejala, total_pengobatan=total_pengobatan, total_pencegahan=total_pencegahan)

@app.route('/gejala') #index
def gejala():
    cursor.execute("SELECT * FROM symptoms")
    symptoms = cursor.fetchall()
    db.commit()
    print(symptoms)

    return render_template('gejaladm.html', symptoms=symptoms)

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
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    cursor.execute("SELECT * FROM preventions")
    preventions = cursor.fetchall()
    db.commit()
    return render_template('addpenyakit.html', treatments=treatments, preventions=preventions)

@app.route('/updatepenyakit')
def updatepenyakit():
    return render_template('updatepenyakit.html')

@app.route('/basis')
def basis():
    return render_template('basisadm.html')

@app.route('/addbasis')
def addbasis():
    cursor.execute("SELECT * FROM symptoms")
    symptoms = cursor.fetchall()
    db.commit()
    return render_template('addbasis.html', symptoms=symptoms)

@app.route('/detailbasis')
def detailbasis():
    return render_template('detailbasis.html')

@app.route('/pengobatan')
def pengobatan():
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    db.commit()
    print(treatments)

    return render_template('pengobatanadm.html', treatments=treatments)

@app.route('/updatepengobatan')
def updatepengobatan():
    return render_template('updatepengobatan.html')

@app.route('/addpengobatan')
def addpengobatan():
    return render_template('addpengobatan.html')

@app.route('/pencegahan')
def pencegahan():
    cursor.execute("SELECT * FROM preventions")
    preventions = cursor.fetchall()
    db.commit()
    print(preventions)

    return render_template('pencegahanadm.html', preventions=preventions)

@app.route('/updatepencegahan')
def updatepencegahan():
    return render_template('updatepencegahan.html')

@app.route('/addpencegahan')
def addpencegahan():
    return render_template('addpencegahan.html')

if __name__ == '__main__':
    app.run (debug = True)