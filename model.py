import pymysql
from config import Config # Mengambil data dari config.py yang kita isi tadi

def get_db_connection():
    """Fungsi untuk membuka gerbang koneksi ke database TiDB Cloud"""
    try:
        connection = pymysql.connect(
            host=Config.TIDB_HOST,
            port=Config.TIDB_PORT,
            user=Config.TIDB_USER,
            password=Config.TIDB_PASSWORD,
            database=Config.TIDB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor # Mengubah hasil query jadi format dictionary (mudah dibaca di frontend)
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error saat menyambungkan ke TiDB Cloud: {e}")
        return None