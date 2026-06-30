from flask import Blueprint, request, jsonify, session
from model import get_db_connection

experience_bp = Blueprint('experience_admin', __name__)

# ==========================================
# 1 & 2. ROUTE UNTUK READ (GET) & CREATE (POST)
# ==========================================
@experience_bp.route('/api/experience', methods=['GET', 'POST'])
def handle_experience():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Database tidak terhubung"}), 500
        
    cursor = conn.cursor()
    
    # JALUR AMBIL DATA (GET)
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM pengalaman ORDER BY id DESC")
            experience = cursor.fetchall()
            cursor.close()
            return jsonify(experience), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()
        
    # JALUR TAMBAH DATA (POST)
    elif request.method == 'POST':
        if not session.get('logged_in'):
            return jsonify({"status": "gagal", "pesan": "Akses ditolak. Silakan login."}), 401

        data = request.get_json()
        perusahaan = data.get('perusahaan')
        posisi = data.get('posisi')
        tahun_mulai = data.get('tahun_mulai')
        tahun_selesai = data.get('tahun_selesai') # Tambahan agar fleksibel

        if not perusahaan or not posisi:
            return jsonify({"status": "gagal", "pesan": "Perusahaan dan Posisi wajib diisi!"}), 400

        try:
            sql = "INSERT INTO pengalaman (perusahaan, posisi, tahun_mulai, tahun_selesai) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (perusahaan, posisi, tahun_mulai, tahun_selesai))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Pengalaman berhasil disimpan!"}), 201
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()

# ==========================================
# 3 & 4. ROUTE UNTUK UPDATE (PUT) & DELETE (DELETE)
# ==========================================
@experience_bp.route('/api/experience/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_experience(id):
    if not session.get('logged_in'):
        return jsonify({"status": "gagal", "pesan": "Akses ditolak. Silakan login."}), 401
        
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Database tidak terhubung"}), 500
    
    cursor = conn.cursor()

    # JALUR UPDATE / UBAH DATA (PUT)
    if request.method == 'PUT':
        data = request.get_json()
        perusahaan = data.get('perusahaan')
        posisi = data.get('posisi')
        tahun_mulai = data.get('tahun_mulai')
        tahun_selesai = data.get('tahun_selesai')

        if not perusahaan or not posisi:
            return jsonify({"status": "gagal", "pesan": "Perusahaan dan Posisi wajib diisi!"}), 400

        try:
            sql = "UPDATE pengalaman SET perusahaan=%s, posisi=%s, tahun_mulai=%s, tahun_selesai=%s WHERE id=%s"
            cursor.execute(sql, (perusahaan, posisi, tahun_mulai, tahun_selesai, id))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Data pengalaman berhasil diperbarui!"}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()

    # JALUR HAPUS DATA (DELETE)
    elif request.method == 'DELETE':
        try:
            sql = "DELETE FROM pengalaman WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Data pengalaman berhasil dihapus!"}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()