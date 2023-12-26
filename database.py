import mysql.connector
from insert import data_treatments, data_preventions, data_symptoms, data_admins
# Inisialisasi db sebagai objek global
db = None

def initialize_database():
    global db
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="xpertdo_trying"
    )

    return db

def get_database_cursor():
    return db.cursor(dictionary = True)

def create_database():
    cursor = get_database_cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(5) PRIMARY KEY, name VARCHAR(255) NOT NULL, age INT, jk CHAR(1) CHECK (jk IN ('L', 'P')), pilihan_gejala VARCHAR(5))")

    cursor.execute("CREATE TABLE IF NOT EXISTS symptoms (kode_gejala VARCHAR(5) PRIMARY KEY, gejala VARCHAR(255) NOT NULL, bobot INT)")

    cursor.execute("CREATE TABLE IF NOT EXISTS treatments (kode_pengobatan VARCHAR(5) PRIMARY KEY, pengobatan VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS preventions (kode_pencegahan VARCHAR(5) PRIMARY KEY, pencegahan VARCHAR(255) NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS admins (email VARCHAR(255) PRIMARY KEY, password VARCHAR(255) NOT NULL)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS diseases (kode_penyakit VARCHAR(5) PRIMARY KEY, penyakit VARCHAR(255) NOT NULL, definisi TEXT, pengobatan1 VARCHAR(255), pengobatan2 VARCHAR(255), pengobatan3 VARCHAR(255), pengobatan4 VARCHAR(255), pengobatan5 VARCHAR(255), pencegahan1 VARCHAR(255), pencegahan2 VARCHAR(255), pencegahan3 VARCHAR(255), pencegahan4 VARCHAR(255), pencegahan5 VARCHAR(255), FOREIGN KEY (pengobatan1) REFERENCES treatments (kode_pengobatan), FOREIGN KEY (pengobatan2) REFERENCES treatments (kode_pengobatan), FOREIGN KEY (pengobatan3) REFERENCES treatments (kode_pengobatan), FOREIGN KEY (pengobatan4) REFERENCES treatments (kode_pengobatan), FOREIGN KEY (pengobatan5) REFERENCES treatments (kode_pengobatan), FOREIGN KEY (pencegahan1) REFERENCES preventions (kode_pencegahan), FOREIGN KEY (pencegahan2) REFERENCES preventions (kode_pencegahan), FOREIGN KEY (pencegahan3) REFERENCES preventions (kode_pencegahan), FOREIGN KEY (pencegahan4) REFERENCES preventions (kode_pencegahan), FOREIGN KEY (pencegahan5) REFERENCES preventions (kode_pencegahan))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS basis (kode_basis VARCHAR(5) PRIMARY KEY, penyakit VARCHAR (255) NOT NULL, gejala1 VARCHAR(255), gejala2 VARCHAR(255), gejala3 VARCHAR(255), gejala4 VARCHAR(255), gejala5 VARCHAR(255), FOREIGN KEY (penyakit) REFERENCES diseases (kode_penyakit), FOREIGN KEY (gejala1) REFERENCES symptoms (kode_gejala), FOREIGN KEY (gejala2) REFERENCES symptoms (kode_gejala), FOREIGN KEY (gejala3) REFERENCES symptoms (kode_gejala), FOREIGN KEY (gejala4) REFERENCES symptoms (kode_gejala), FOREIGN KEY (gejala5) REFERENCES symptoms (kode_gejala))""")

    cursor.close()

def id_user():
    cursor = get_database_cursor()

    cursor.execute("SELECT user_id FROM users ORDER BY user_id DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['user_id']:
        last_idu = result['user_id']
        next_idu = f'#{int(last_idu[1:]) + 1:02d}'
    else:
        next_idu = '#01'

    cursor.close()

    return next_idu

def kode_gejala():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_gejala FROM symptoms ORDER BY kode_gejala DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_gejala']:
        last_ipg = result['kode_gejala']
        prefix = last_ipg[:-2]  # Mengambil semua karakter kecuali dua karakter terakhir
        numeric_part = int(last_ipg[-2:]) + 1  # Menambahkan satu ke dua karakter terakhir dan mengonversinya ke integer
        next_ipg = f'{prefix}{numeric_part:02d}'
    else:
        next_ipg = 'G01'

    cursor.close()

    return next_ipg

def kode_pengobatan():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_pengobatan FROM treatments ORDER BY kode_pengobatan DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_pengobatan']:
        last_ipg = result['kode_pengobatan']
        prefix = last_ipg[:-2]  # Mengambil semua karakter kecuali dua karakter terakhir
        numeric_part = int(last_ipg[-2:]) + 1  # Menambahkan satu ke dua karakter terakhir dan mengonversinya ke integer
        next_ipg = f'{prefix}{numeric_part:02d}'
    else:
        next_ipg = 'PN01'

    cursor.close()

    return next_ipg

def kode_pencegahan():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_pencegahan FROM preventions ORDER BY kode_pencegahan DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_pencegahan']:
        last_ipg = result['kode_pencegahan']
        prefix = last_ipg[:-2]  # Mengambil semua karakter kecuali dua karakter terakhir
        numeric_part = int(last_ipg[-2:]) + 1  # Menambahkan satu ke dua karakter terakhir dan mengonversinya ke integer
        next_ipg = f'{prefix}{numeric_part:02d}'
    else:
        next_ipg = 'PG01'

    cursor.close()

    return next_ipg

def kode_penyakit():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_penyakit FROM diseases ORDER BY kode_penyakit DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_penyakit']:
        last_ipp = result['kode_penyakit']
        prefix = last_ipp[:-2]  # Mengambil semua karakter kecuali dua karakter terakhir
        numeric_part = int(last_ipp[-2:]) + 1  # Menambahkan satu ke dua karakter terakhir dan mengonversinya ke integer
        next_ipp = f'{prefix}{numeric_part:02d}'
    else:
        next_ipp = 'P01'

    cursor.close()

    return next_ipp

def kode_basis():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_basis FROM basis ORDER BY kode_basis DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_basis']:
        last_ipb = result['kode_basis']
        prefix = last_ipb[:-2]  # Mengambil semua karakter kecuali dua karakter terakhir
        numeric_part = int(last_ipb[-2:]) + 1  # Menambahkan satu ke dua karakter terakhir dan mengonversinya ke integer
        next_ipb = f'{prefix}{numeric_part:02d}'
    else:
        next_ipb = 'B01'

    cursor.close()

    return next_ipb

def insert_symptoms():
    try:
        cursor = get_database_cursor()

        for symptom in data_symptoms:
            cursor.execute("SELECT COUNT(*) as count FROM symptoms WHERE kode_gejala = %s", (symptom['kode_gejala'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                # Jika kode_gejala belum ada, maka masukkan data
                cursor.execute(
                    "INSERT INTO symptoms (kode_gejala, gejala, bobot) VALUES (%s, %s, %s)",
                    (symptom['kode_gejala'], symptom['gejala'], symptom['bobot'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()

def insert_preventions():
    try:
        cursor = get_database_cursor()

        for prevention in data_preventions:
            # Check if the kode_pencegahan already exists
            cursor.execute("SELECT COUNT(*) as count FROM preventions WHERE kode_pencegahan = %s", (prevention['kode_pencegahan'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                # Jika kode_pencegahan belum ada, maka masukkan data
                cursor.execute(
                    "INSERT INTO preventions (kode_pencegahan, pencegahan) VALUES (%s, %s)",
                    (prevention['kode_pencegahan'], prevention['pencegahan'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()


def insert_treatments():
    try:
        cursor = get_database_cursor()

        for treatment in data_treatments:
            # Check if the kode_pengobatan already exists
            cursor.execute("SELECT COUNT(*) as count FROM treatments WHERE kode_pengobatan = %s", (treatment['kode_pengobatan'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                # Jika kode_pengobatan belum ada, maka masukkan data
                cursor.execute(
                    "INSERT INTO treatments (kode_pengobatan, pengobatan) VALUES (%s, %s)",
                    (treatment['kode_pengobatan'], treatment['pengobatan'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()


def insert_admins():
    try:
        cursor = get_database_cursor()

        for admin in data_admins:
            cursor.execute("SELECT COUNT(*) as count FROM admins WHERE email = %s", (admin['email'],))
            result = cursor.fetchone()

            if result and result['count'] == 0:
                cursor.execute(
                    "INSERT INTO admins (email, password) VALUES (%s, %s)",
                    (admin['email'], admin['password'])
                )

        db.commit()

    except Exception as e:
        print("Error:", str(e))
        db.rollback()

    finally:
        cursor.close()


def check_admin_credentials(email, password):
    cursor = get_database_cursor()
    query = "SELECT * FROM admins WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def get_prevention_by_code(kode_pencegahan):
    cursor = get_database_cursor()
    query = "SELECT * FROM preventions WHERE kode_pencegahan = %s"
    cursor.execute(query, (kode_pencegahan,))
    prevention = cursor.fetchone()
    cursor.close()
    return prevention

def update_prevention(kode_pencegahan, new_data):
    try:
        cursor = get_database_cursor()
        cursor.execute("UPDATE preventions SET pencegahan = %s WHERE kode_pencegahan = %s",
                       (new_data['pencegahan'], kode_pencegahan))
        db.commit()
        return True

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False

    finally:
        cursor.close()

def get_treatment_by_code(kode_pengobatan):
    cursor = get_database_cursor()
    query = "SELECT * FROM treatments WHERE kode_pengobatan = %s"
    cursor.execute(query, (kode_pengobatan,))
    treatment = cursor.fetchone()
    cursor.close()
    return treatment

def update_treatment(kode_pengobatan, new_data):
    try:
        cursor = get_database_cursor()
        cursor.execute("UPDATE treatments SET pengobatan = %s WHERE kode_pengobatan = %s",
                       (new_data['pengobatan'], kode_pengobatan))
        db.commit()
        return True

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False

    finally:
        cursor.close()

def get_symptom_by_code(kode_gejala):
    cursor = get_database_cursor()
    query = "SELECT * FROM symptoms WHERE kode_gejala = %s"
    cursor.execute(query, (kode_gejala,))
    symptom = cursor.fetchone()
    cursor.close()
    return symptom

def update_symptom(kode_gejala, new_data):
    try:
        cursor = get_database_cursor()
        cursor.execute("UPDATE symptoms SET gejala = %s, bobot = %s WHERE kode_gejala = %s" ,
                       (new_data['gejala'], new_data['bobot'], kode_gejala))
        db.commit()
        return True

    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False

    finally:
        cursor.close()

def add_prevention(data):
    try:
        cursor = get_database_cursor()
        cursor.execute("INSERT INTO preventions (kode_pencegahan, pencegahan) VALUES (%s, %s)",
                       (data['kode_pencegahan'], data['pencegahan']))
        db.commit()
        return True
    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def add_treatment(data):
    try:
        cursor = get_database_cursor()
        cursor.execute("INSERT INTO treatments (kode_pengobatan, pengobatan) VALUES (%s, %s)",
                       (data['kode_pengobatan'], data['pengobatan']))
        db.commit()
        return True
    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def add_symptom(data):
    try:
        cursor = get_database_cursor()
        cursor.execute("INSERT INTO symptoms (kode_gejala, gejala, bobot) VALUES (%s, %s, %s)",
                       (data['kode_gejala'], data['gejala'], data['bobot']))
        db.commit()
        return True
    except Exception as e:
        print("Error:", str(e))
        db.rollback()
        return False
    finally:
        if cursor:
            cursor.close()

def save_to_diseases_table(id_penyakit, nama_penyakit, definisi, pengobatan1, pengobatan2, pengobatan3, pengobatan4, pengobatan5,
                           pencegahan1, pencegahan2, pencegahan3, pencegahan4, pencegahan5):
    cursor = get_database_cursor()
    try:
        # Eksekusi query SQL untuk menyimpan data ke tabel diseases
        insert_query = "INSERT INTO diseases (kode_penyakit, penyakit, definisi, pengobatan1, pengobatan2, pengobatan3, pengobatan4, pengobatan5, pencegahan1, pencegahan2, pencegahan3, pencegahan4, pencegahan5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        params = (
            id_penyakit, nama_penyakit, definisi,
            pengobatan1 if pengobatan1 and pengobatan1 != 'NONE' else None,
            pengobatan2 if pengobatan2 and pengobatan2 != 'NONE' else None,
            pengobatan3 if pengobatan3 and pengobatan3 != 'NONE' else None,
            pengobatan4 if pengobatan4 and pengobatan4 != 'NONE' else None,
            pengobatan5 if pengobatan5 and pengobatan5 != 'NONE' else None,
            pencegahan1 if pencegahan1 and pencegahan1 != 'NONE' else None,
            pencegahan2 if pencegahan2 and pencegahan2 != 'NONE' else None,
            pencegahan3 if pencegahan3 and pencegahan3 != 'NONE' else None,
            pencegahan4 if pencegahan4 and pencegahan4 != 'NONE' else None,
            pencegahan5 if pencegahan5 and pencegahan5 != 'NONE' else None,
        )
        # Mengeksekusi query SQL yang telah dibangun dan mencoba mengeksekusi perubahan yang diminta
        with db.cursor() as cursor:
            cursor.execute(insert_query, params)
            db.commit()
            print(insert_query)
    except Exception as e:
        print("Error during insert:", str(e))
        db.rollback()

def save_to_basis_table(id_basis, nama_penyakit, gejala1, gejala2, gejala3, gejala4, gejala5):
    cursor = get_database_cursor()
    try:
        # Eksekusi query SQL untuk menyimpan data ke tabel basis
        insert_query = "INSERT INTO basis (kode_basis, penyakit, gejala1, gejala2, gejala3, gejala4, gejala5) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        params = (
            id_basis, nama_penyakit,
            gejala1 if gejala1 and gejala1 != 'NONE' else None,
            gejala2 if gejala2 and gejala2 != 'NONE' else None,
            gejala3 if gejala3 and gejala3 != 'NONE' else None,
            gejala4 if gejala4 and gejala4 != 'NONE' else None,
            gejala5 if gejala5 and gejala5 != 'NONE' else None,
        )
        # Mengeksekusi query SQL yang telah dibangun dan mencoba mengeksekusi perubahan yang diminta
        with db.cursor() as cursor:
            cursor.execute(insert_query, params)
            db.commit()
    except Exception as e:
        print("Error during insert:", str(e))
        db.rollback()


def get_treatments():
    cursor = get_database_cursor()
    cursor.execute("SELECT * FROM treatments")
    return cursor.fetchall()

# Fungsi untuk mendapatkan data pencegahan dari tabel pencegahan
def get_preventions():
    cursor = get_database_cursor()
    cursor.execute("SELECT * FROM preventions")
    return cursor.fetchall()

def get_diseases():
    cursor = get_database_cursor()
    cursor.execute("SELECT * FROM diseases")
    return cursor.fetchall()

# Fungsi untuk mendapatkan data pencegahan dari tabel pencegahan
def get_symptoms():
    cursor = get_database_cursor()
    cursor.execute("SELECT * FROM symptoms")
    return cursor.fetchall()

def get_disease_by_code(kode_penyakit):
    cursor = get_database_cursor()
    query = "SELECT * FROM diseases WHERE kode_penyakit = %s"
    cursor.execute(query, (kode_penyakit,))
    result = cursor.fetchone()
    cursor.close()
    return result

def update_disease(kode_penyakit, new_data):
    cursor = get_database_cursor()
    try:
        # Menggunakan kode_penyakit dan data baru untuk membangun query SQL yang mengubah data penyakit di database
        query = """UPDATE diseases SET penyakit = %s, definisi = %s, pengobatan1 = %s, pengobatan2 = %s, pengobatan3 = %s, pengobatan4 = %s, pengobatan5 = %s, pencegahan1 = %s, pencegahan2 = %s, pencegahan3 = %s, pencegahan4 = %s, pencegahan5 = %s WHERE kode_penyakit = %s"""

        params = (
            new_data['penyakit'], new_data['definisi'],
            new_data['pengobatan1'] if new_data['pengobatan1'] and new_data['pengobatan1'] != 'NONE' else None,
            new_data['pengobatan2'] if new_data['pengobatan2'] and new_data['pengobatan2'] != 'NONE' else None,
            new_data['pengobatan3'] if new_data['pengobatan3'] and new_data['pengobatan3'] != 'NONE' else None,
            new_data['pengobatan4'] if new_data['pengobatan4'] and new_data['pengobatan4'] != 'NONE' else None,
            new_data['pengobatan5'] if new_data['pengobatan5'] and new_data['pengobatan5'] != 'NONE' else None,
            new_data['pencegahan1'] if new_data['pencegahan1'] and new_data['pencegahan1'] != 'NONE' else None,
            new_data['pencegahan2'] if new_data['pencegahan2'] and new_data['pencegahan2'] != 'NONE' else None,
            new_data['pencegahan3'] if new_data['pencegahan3'] and new_data['pencegahan3'] != 'NONE' else None,
            new_data['pencegahan4'] if new_data['pencegahan4'] and new_data['pencegahan4'] != 'NONE' else None,
            new_data['pencegahan5'] if new_data['pencegahan5'] and new_data['pencegahan5'] != 'NONE' else None,
            kode_penyakit
        )
        # Mengeksekusi query SQL yang telah dibangun dan mencoba mengeksekusi perubahan yang diminta
        with db.cursor() as cursor:
            cursor.execute(query, params)
            db.commit()

        return True
    except Exception as e:
        print(f"Gagal memperbarui penyakit: {e}")
        return False

def get_basis_details(kode_basis):
    cursor = get_database_cursor()
    # Ambil detail penyakit dari tabel basis
    cursor.execute('SELECT * FROM basis WHERE kode_basis = %s', (kode_basis,))
    basis_data = cursor.fetchone()

    # Ambil gejala untuk penyakit tertentu dari tabel basis_gejala
    cursor.execute('SELECT * FROM basis_gejala WHERE kode_basis = %s', (kode_basis,))
    symptoms_data = cursor.fetchall()

    # Tutup koneksi database
    cursor.close()
    db.close()

    # Format data ke dalam bentuk dictionary
    disease = {
        'name': basis_data['penyakit'],
        'definition': basis_data['definisi'],
        'symptoms': [{'id': symptom['id_gejala'], 'name': symptom['gejala'], 'weight': symptom['bobot']} for symptom in symptoms_data],
        # Tambahkan detail lain jika diperlukan
    }

    return disease

def get_detail_basis(kode_basis):
    try:
        cursor = get_database_cursor()

        # Menjalankan query SQL untuk mendapatkan detail basis
        query = """ 
        SELECT basis.kode_basis,
            diseases.penyakit, diseases.definisi,
            symptoms1.kode_gejala AS kode_gejala1, symptoms1.gejala AS gejala1, symptoms1.bobot AS bobot1,
            symptoms2.kode_gejala AS kode_gejala2, symptoms2.gejala AS gejala2, symptoms2.bobot AS bobot2,
            symptoms3.kode_gejala AS kode_gejala3, symptoms3.gejala AS gejala3, symptoms3.bobot AS bobot3,
            symptoms4.kode_gejala AS kode_gejala4, symptoms4.gejala AS gejala4, symptoms4.bobot AS bobot4,
            symptoms5.kode_gejala AS kode_gejala5, symptoms5.gejala AS gejala5, symptoms5.bobot AS bobot5,
            treatments.kode_pengobatan AS kode_pengobatan1, treatments.pengobatan AS pengobatan1,
            treatments2.kode_pengobatan AS kode_pengobatan2, treatments2.pengobatan AS pengobatan2,
            treatments3.kode_pengobatan AS kode_pengobatan3, treatments3.pengobatan AS pengobatan3,
            treatments4.kode_pengobatan AS kode_pengobatan4, treatments4.pengobatan AS pengobatan4,
            treatments5.kode_pengobatan AS kode_pengobatan5, treatments5.pengobatan AS pengobatan5,
            preventions.kode_pencegahan AS kode_pencegahan1, preventions.pencegahan AS pencegahan1,
            preventions2.kode_pencegahan AS kode_pencegahan2, preventions2.pencegahan AS pencegahan2,
            preventions3.kode_pencegahan AS kode_pencegahan3, preventions3.pencegahan AS pencegahan3,
            preventions4.kode_pencegahan AS kode_pencegahan4, preventions4.pencegahan AS pencegahan4,
            preventions5.kode_pencegahan AS kode_pencegahan5, preventions5.pencegahan AS pencegahan5
        FROM basis
        JOIN diseases ON basis.penyakit = diseases.kode_penyakit
        LEFT JOIN symptoms AS symptoms1 ON basis.gejala1 = symptoms1.kode_gejala
        LEFT JOIN symptoms AS symptoms2 ON basis.gejala2 = symptoms2.kode_gejala
        LEFT JOIN symptoms AS symptoms3 ON basis.gejala3 = symptoms3.kode_gejala
        LEFT JOIN symptoms AS symptoms4 ON basis.gejala4 = symptoms4.kode_gejala
        LEFT JOIN symptoms AS symptoms5 ON basis.gejala5 = symptoms5.kode_gejala
        LEFT JOIN treatments ON diseases.pengobatan1 = treatments.kode_pengobatan
        LEFT JOIN treatments AS treatments2 ON diseases.pengobatan2 = treatments2.kode_pengobatan
        LEFT JOIN treatments AS treatments3 ON diseases.pengobatan3 = treatments3.kode_pengobatan
        LEFT JOIN treatments AS treatments4 ON diseases.pengobatan4 = treatments4.kode_pengobatan
        LEFT JOIN treatments AS treatments5 ON diseases.pengobatan5 = treatments5.kode_pengobatan
        LEFT JOIN preventions ON diseases.pencegahan1 = preventions.kode_pencegahan
        LEFT JOIN preventions AS preventions2 ON diseases.pencegahan2 = preventions2.kode_pencegahan
        LEFT JOIN preventions AS preventions3 ON diseases.pencegahan3 = preventions3.kode_pencegahan
        LEFT JOIN preventions AS preventions4 ON diseases.pencegahan4 = preventions4.kode_pencegahan
        LEFT JOIN preventions AS preventions5 ON diseases.pencegahan5 = preventions5.kode_pencegahan
        WHERE basis.kode_basis = %s"""

        cursor.execute(query, (kode_basis,))

        data = cursor.fetchone()

        cursor.close()

        return data

    except Exception as e:
        return str(e)

