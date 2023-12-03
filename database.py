import mysql.connector

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

    # Membuat tabel users jika belum ada
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR(5) PRIMARY KEY, name VARCHAR(255) NOT NULL, age INT, jk CHAR(1) CHECK (jk IN ('L', 'P')), pilihan_gejala VARCHAR(5))")

    # Membuat tabel symptom jika belum ada
    cursor.execute("CREATE TABLE IF NOT EXISTS symptoms (kode_gejala VARCHAR(5) PRIMARY KEY, gejala VARCHAR(255) NOT NULL, bobot INT)")

    cursor.close()

def id_user():
    cursor = get_database_cursor()

    cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    if result and result[0]:
        last_idu = result[0]
        last_number = int(last_idu[1:])
        next_idu = f'#{last_number + 1:02d}'
    else:
        next_idu = '#01'

    cursor.close()

    return next_idu


def kode_gejala():
    cursor = get_database_cursor()

    cursor.execute("SELECT kode_gejala FROM symptoms ORDER BY kode_gejala DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        last_idg = result[0]
        next_idg = f'G{int(last_idg[1:]) + 1:02d}'
    else:
        next_idg = 'G01'

    cursor.close()

    return next_idg