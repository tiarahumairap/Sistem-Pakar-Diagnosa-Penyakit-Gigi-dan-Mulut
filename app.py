from flask import Flask, render_template, request, redirect, url_for, session
from database import initialize_database, create_database, id_user, get_database_cursor, db, insert_treatments, insert_preventions, insert_symptoms, insert_admins, check_admin_credentials, get_prevention_by_code, update_prevention, get_treatment_by_code, update_treatment, get_symptom_by_code, update_symptom, add_prevention, kode_pencegahan, kode_pengobatan, add_treatment, add_symptom, kode_gejala, kode_penyakit, save_to_diseases_table, get_treatments, get_preventions, update_disease, kode_penyakit, get_disease_by_code, kode_basis, get_symptoms, get_diseases, save_to_basis_table, get_detail_basis

app = Flask(__name__)
app.secret_key = 'ara20102196ara'

db = initialize_database()
cursor = get_database_cursor()
create_database()
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

        selected_symptom_codes = request.form.getlist('gejala')
        print("Kode Gejala yang dicentang:", selected_symptom_codes)

        # Gabungkan nilai gejala menjadi string
        pilihan_kode_gejala = ",".join(selected_symptom_codes)

        # Dapatkan ID terakhir yang terdaftar dalam tabel users
        cursor.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            last_idu = result['user_id']
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

    return render_template('gejaladm.html', symptoms=symptoms)

@app.route('/addgejala', methods=['GET', 'POST'])
def addgejala():
    kode_gejala_value = kode_gejala()
    if request.method == 'POST':
        new_data = {
            'kode_gejala': kode_gejala_value,
            'gejala': request.form.get('gejala'),
            'bobot': request.form.get('bobot')
        }

        if add_symptom(new_data):
            return redirect(url_for('gejala'))
        else:
            return render_template('addgejala.html', error="Gagal menambahkan gejala")

    else:
        return render_template('addgejala.html', kode_gejala=kode_gejala_value)

@app.route('/updategejala/<kode_gejala>', methods = ['GET', 'POST'])
def updategejala(kode_gejala):
    if request.method == 'POST':
        new_data = {
            'gejala': request.form.get('gejala'),
            'bobot': request.form.get('bobot')
        }

        if update_symptom(kode_gejala, new_data):
            return redirect(url_for('gejala'))
        else:
            return render_template('updategejala.html', error="Gagal memperbarui gejala")

    else:
        symptom = get_symptom_by_code(kode_gejala)
        return render_template('updategejala.html', symptom=symptom)

@app.route('/penyakit')
def penyakit():
    cursor.execute("SELECT * FROM diseases")
    diseases = cursor.fetchall()
    db.commit()

    return render_template('penyakitadm.html', diseases=diseases)

@app.route('/updatepenyakit/<kode_penyakit>', methods=['GET', 'POST'])
def updatepenyakit(kode_penyakit):
    treatments = get_treatments()
    preventions = get_preventions()

    if request.method == 'POST':
        new_data = {
            'penyakit': request.form.get('penyakit'),
            'definisi': request.form.get('definisi'),
            'pengobatan1': request.form.get('pengobatan1'),
            'pengobatan2': request.form.get('pengobatan2'),
            'pengobatan3': request.form.get('pengobatan3'),
            'pengobatan4': request.form.get('pengobatan4'),
            'pengobatan5': request.form.get('pengobatan5'),
            'pencegahan1': request.form.get('pencegahan1'),
            'pencegahan2': request.form.get('pencegahan2'),
            'pencegahan3': request.form.get('pencegahan3'),
            'pencegahan4': request.form.get('pencegahan4'),
            'pencegahan5': request.form.get('pencegahan5')
        }

        # Tambahkan kode_penyakit ke new_data
        new_data['kode_penyakit'] = kode_penyakit

        if update_disease(kode_penyakit, new_data):
            return redirect(url_for('penyakit'))
        else:
            return render_template('updatepenyakit.html', error="Gagal memperbarui penyakit")

    else:
        disease = get_disease_by_code(kode_penyakit)
        return render_template('updatepenyakit.html', disease=disease, treatments=treatments, preventions=preventions)

@app.route('/basis')
def basis():
    try:
        # Buka koneksi ke database dan dapatkan cursor
        cursor = get_database_cursor()

        # Eksekusi query
        cursor.execute("""
            SELECT basis.kode_basis, diseases.penyakit,
                SUM(
                    CASE WHEN basis.gejala1 IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN basis.gejala2 IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN basis.gejala3 IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN basis.gejala4 IS NOT NULL THEN 1 ELSE 0 END +
                    CASE WHEN basis.gejala5 IS NOT NULL THEN 1 ELSE 0 END
                ) AS jumlah_gejala
            FROM basis
            JOIN diseases ON basis.penyakit = diseases.kode_penyakit
            GROUP BY basis.kode_basis, diseases.penyakit
        """)

        # Ambil hasil query
        basis = cursor.fetchall()

        return render_template('basisadm.html', basis=basis)

    except Exception as e:
        # Handle exception (contohnya, print pesan error)
        print("Error:", str(e))

    finally:
        # Pastikan untuk menutup cursor dan koneksi setelah selesai
        cursor.close()
        db.close()

@app.route('/addbasis', methods=['GET', 'POST'])
def addbasis():
    if request.method == 'POST':
        id_basis = kode_basis()
        nama_penyakit = request.form.get('penyakit')
        gejala1 = request.form.get('gejala1')
        gejala2 = request.form.get('gejala2')
        gejala3 = request.form.get('gejala3')
        gejala4 = request.form.get('gejala4')
        gejala5 = request.form.get('gejala5')

        save_to_basis_table(id_basis, nama_penyakit, gejala1, gejala2, gejala3, gejala4, gejala5)
        # Redirect ke halaman basis
        return redirect(url_for('basis'))
    # Perbarui dropdown untuk basis dan pencegahan
    diseases = get_diseases()
    symptoms = get_symptoms()
    id_basis = kode_basis()

    return render_template('addbasis.html', diseases=diseases, symptoms=symptoms, kode_basis=id_basis)

@app.route('/detailbasis/<kode_basis>', methods=['GET', 'POST'])
def detailbasis(kode_basis):
    data = get_detail_basis(kode_basis)

    return render_template('detailbasis.html', data=data)

@app.route('/pengobatan')
def pengobatan():
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    db.commit()
    print(treatments)

    return render_template('pengobatanadm.html', treatments=treatments)

@app.route('/updatepengobatan/<kode_pengobatan>', methods=['GET', 'POST'])
def updatepengobatan(kode_pengobatan):
    if request.method == 'POST':
        new_data = {
            'pengobatan': request.form.get('pengobatan')
        }

        if update_treatment(kode_pengobatan, new_data):
            return redirect(url_for('pengobatan'))
        else:
            return render_template('updatepengobatan.html', error="Gagal memperbarui pengobatan")

    else:
        treatment = get_treatment_by_code(kode_pengobatan)
        return render_template('updatepengobatan.html', treatment=treatment)

@app.route('/addpengobatan', methods=['GET', 'POST'])
def addpengobatan():
    kode_pengobatan_value = kode_pengobatan()
    if request.method == 'POST':
        new_data = {
            'kode_pengobatan': kode_pengobatan_value,
            'pengobatan': request.form.get('pengobatan')
        }

        if add_treatment(new_data):
            return redirect(url_for('pengobatan'))
        else:
            return render_template('addpengobatan.html', error="Gagal menambahkan pengobatan")
    else:
        # Metode GET, melewati nilai kode_pengobatan ke template
        return render_template('addpengobatan.html', kode_pengobatan=kode_pengobatan_value)

@app.route('/pencegahan')
def pencegahan():
    cursor.execute("SELECT * FROM preventions")
    preventions = cursor.fetchall()
    db.commit()
    print(preventions)

    return render_template('pencegahanadm.html', preventions=preventions)

@app.route('/updatepencegahan/<kode_pencegahan>', methods=['GET', 'POST'])
def updatepencegahan(kode_pencegahan):
    if request.method == 'POST':
        new_data = {
            'pencegahan': request.form.get('pencegahan')
        }

        if update_prevention(kode_pencegahan, new_data):
            return redirect(url_for('pencegahan'))
        else:
            return render_template('updatepencegahan.html', error="Gagal memperbarui pencegahan")

    else:
        prevention = get_prevention_by_code(kode_pencegahan)
        return render_template('updatepencegahan.html', prevention=prevention)

@app.route('/addpencegahan', methods=['GET', 'POST'])
def addpencegahan():
    kode_pencegahan_value = kode_pencegahan()
    if request.method == 'POST':
        new_data = {
            'kode_pencegahan': kode_pencegahan_value,
            'pencegahan': request.form.get('pencegahan')
        }

        if add_prevention(new_data):
            return redirect(url_for('pencegahan'))
        else:
            return render_template('addpencegahan.html', error="Gagal menambahkan pencegahan")

    else:
        return render_template('addpencegahan.html', kode_pencegahan=kode_pencegahan_value)

from flask import request, jsonify

@app.route('/deletegejala/<kode_gejala>', methods=['DELETE'])
def deletegejala(kode_gejala):
    try:

        # Cek apakah gejala dengan kode_gejala tertentu ada di database
        cursor.execute("SELECT * FROM symptoms WHERE kode_gejala = %s", (kode_gejala,))
        gejala = cursor.fetchone()

        if gejala:
            # Hapus gejala dari database
            cursor.execute("DELETE FROM symptoms WHERE kode_gejala = %s", (kode_gejala,))
            db.commit()
            return 'Gejala berhasil dihapus', 200
        else:
            return 'Gejala tidak ditemukan', 404

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return 'Terjadi kesalahan', 500

    finally:
        cursor.close()

@app.route('/deletepencegahan/<kode_pencegahan>', methods=['DELETE'])
def deletepencegahan(kode_pencegahan):
    try:

        # Cek apakah pencegahan dengan kode_pencegahan tertentu ada di database
        cursor.execute("SELECT * FROM preventions WHERE kode_pencegahan = %s", (kode_pencegahan,))
        pencegahan = cursor.fetchone()

        if pencegahan:
            # Hapus pencegahan dari database
            cursor.execute("DELETE FROM preventions WHERE kode_pencegahan = %s", (kode_pencegahan,))
            db.commit()
            return 'Pencegahan berhasil dihapus', 200
        else:
            return 'Pencegahan tidak ditemukan', 404

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return 'Terjadi kesalahan', 500

    finally:
        cursor.close()

@app.route('/deletepengobatan/<kode_pengobatan>', methods=['DELETE'])
def deletepengobatan(kode_pengobatan):
    try:

        # Cek apakah pengobatan dengan kode_pengobatan tertentu ada di database
        cursor.execute("SELECT * FROM treatments WHERE kode_pengobatan = %s", (kode_pengobatan,))
        pengobatan = cursor.fetchone()

        if pengobatan:
            # Hapus pengobatan dari database
            cursor.execute("DELETE FROM treatments WHERE kode_pengobatan = %s", (kode_pengobatan,))
            db.commit()
            return 'Pengobatan berhasil dihapus', 200
        else:
            return 'Pengobatan tidak ditemukan', 404

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return 'Terjadi kesalahan', 500

    finally:
        cursor.close()

@app.route('/addpenyakit', methods=['GET', 'POST'])
def addpenyakit():
    if request.method == 'POST':
        id_penyakit = kode_penyakit()
        nama_penyakit = request.form.get('penyakit')
        definisi = request.form.get('definisi')
        pengobatan1 = request.form.get('pengobatan1')
        pengobatan2 = request.form.get('pengobatan2')
        pengobatan3 = request.form.get('pengobatan3')
        pengobatan4 = request.form.get('pengobatan4')
        pengobatan5 = request.form.get('pengobatan5')
        pencegahan1 = request.form.get('pencegahan1')
        pencegahan2 = request.form.get('pencegahan2')
        pencegahan3 = request.form.get('pencegahan3')
        pencegahan4 = request.form.get('pencegahan4')
        pencegahan5 = request.form.get('pencegahan5')


        save_to_diseases_table(id_penyakit, nama_penyakit, definisi, pengobatan1, pengobatan2, pengobatan3, pengobatan4, pengobatan5, pencegahan1, pencegahan2, pencegahan3, pencegahan4, pencegahan5)

        # Redirect ke halaman penyakit
        return redirect(url_for('penyakit'))

    # Perbarui dropdown untuk pengobatan dan pencegahan
    treatments = get_treatments()
    preventions = get_preventions()

    # Jika metode GET, tampilkan formulir
    id_penyakit = kode_penyakit()
    return render_template('addpenyakit.html', treatments=treatments, preventions=preventions, kode_penyakit=id_penyakit)

@app.route('/deletepenyakit/<kode_penyakit>', methods=['DELETE'])
def deletepenyakit(kode_penyakit):
    try:

        # Cek apakah penyakit dengan kode_penyakit tertentu ada di database
        cursor.execute("SELECT * FROM diseases WHERE kode_penyakit = %s", (kode_penyakit,))
        penyakit = cursor.fetchone()

        if penyakit:
            # Hapus penyakit dari database
            cursor.execute("DELETE FROM diseases WHERE kode_penyakit = %s", (kode_penyakit,))
            db.commit()
            return 'penyakit berhasil dihapus', 200
        else:
            return 'penyakit tidak ditemukan', 404

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return 'Terjadi kesalahan', 500

    finally:
        cursor.close()

@app.route('/deletebasis/<kode_basis>', methods=['DELETE'])
def deletebasis(kode_basis):
    try:
        # Cek apakah basis dengan kode_basis tertentu ada di database
        cursor.execute("SELECT * FROM basis WHERE kode_basis = %s", (kode_basis,))
        basis = cursor.fetchone()

        if basis:
            # Hapus basis dari database
            cursor.execute("DELETE FROM basis WHERE kode_basis = %s", (kode_basis,))
            db.commit()
            return 'basis berhasil dihapus', 200
        else:
            return 'basis tidak ditemukan', 404

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return 'Terjadi kesalahan', 500

    finally:
        cursor.close()

if __name__ == '__main__':
    app.run (debug = True)