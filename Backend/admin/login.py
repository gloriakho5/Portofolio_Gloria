from flask import Blueprint, request, jsonify, session
from model import get_db_connection

# Membuat Blueprint Flask khusus untuk menangani admin login
login_bp = Blueprint('login_admin', __name__)

@login_bp.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "gagal", "pesan": "Username dan password wajib diisi!"}), 400 

    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Koneksi ke database bermasalah."}), 500

    try:
        with conn.cursor() as cursor:
            # Mencari data admin di tabel admin yang sudah di-run di TiDB sebelumnya
            sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            admin = cursor.fetchone()

            if admin:
                # Jika data cocok, simpan status login di dalam session server
                session['logged_in'] = True
                session['username'] = admin['username']
                return jsonify({"status": "sukses", "pesan": "Login berhasil! Selamat datang Admin."}), 200
            else:
                return jsonify({"status": "gagal", "pesan": "Username atau password salah."}), 401
    finally:
        conn.close()

@login_bp.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    # Menghapus session untuk proses logout
    session.clear()
    return jsonify({"status": "sukses", "pesan": "Berhasil logout."}), 200