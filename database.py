import mysql.connector
from insert import data_treatments, data_preventions, data_symptoms

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
        last_idg = result['kode_gejala']
        next_idg = f'G{int(last_idg[1:]) + 1:02d}'
    else:
        next_idg = 'G01'

    cursor.close()

    return next_idg

def kode_pengobatan():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_pengobatan FROM treatments ORDER BY kode_pengobatan DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_pengobatan']:
        last_ipn = result['kode_pengobatan']
        next_ipn = f'PN{int(last_ipn[1:]) + 1:02d}'
    else:
        next_ipn = 'PN01'

    cursor.close()

    return next_ipn

def kode_pencegahan():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_pencegahan FROM preventions ORDER BY kode_pencegahan DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result['kode_pencegahan']:
        last_ipg = result['kode_pencegahan']
        next_ipg = f'PG{int(last_ipg[1:]) + 1:02d}'
    else:
        next_ipg = 'PG01'

    cursor.close()

    return next_ipg

def insert_symptoms():
    try:
        cursor = get_database_cursor()

        for symptom in data_symptoms:
            # Check if the kode_pencegahan already exists
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

