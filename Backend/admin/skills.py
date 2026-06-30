from flask import Blueprint, request, jsonify, session
from model import get_db_connection

# KUNCI UTAMA: Nama variabel HARUS 'skills_bp' agar terbaca oleh app.py
skills_bp = Blueprint('skills_admin', __name__)

@skills_bp.route('/api/admin/skills', methods=['GET', 'POST'])
def handle_skills():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Database tidak terhubung"}), 500
        
    cursor = conn.cursor()
    
    # 1. JALUR AMBIL DATA (GET)
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM skill ORDER BY id DESC")
            skills = cursor.fetchall()
            cursor.close()
            return jsonify({"status": "sukses", "data": skills}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()
        
    # 2. JALUR TAMBAH DATA (POST)
    elif request.method == 'POST':
        if not session.get('logged_in'):
            return jsonify({"status": "gagal", "pesan": "Akses ditolak. Silakan login."}), 401
            
        data = request.get_json()
        nama_skill = data.get('nama_skill')
        
        if not nama_skill:
            return jsonify({"status": "gagal", "pesan": "Nama skill wajib diisi!"}), 400
            
        try:
            cursor.execute("INSERT INTO skill (nama_skill) VALUES (%s)", (nama_skill,))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Keahlian berhasil ditambahkan!"}), 201
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()