from flask import Blueprint, request, jsonify, session
from model import get_db_connection

projects_bp = Blueprint('projects_admin', __name__)

# ==========================================
# 1 & 2. ROUTE READ (GET) & CREATE (POST)
# ==========================================
@projects_bp.route('/api/admin/projects', methods=['GET', 'POST'])
def handle_projects():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Database tidak terhubung"}), 500
    cursor = conn.cursor()

    # JALUR AMBIL DATA (GET)
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM proyek ORDER BY id DESC")
            projects = cursor.fetchall()
            cursor.close()
            return jsonify({"status": "sukses", "data": projects}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()

    # JALUR TAMBAH DATA (POST)
    elif request.method == 'POST':
        if not session.get('logged_in'):
            return jsonify({"status": "gagal", "pesan": "Akses ditolak"}), 401

        data = request.get_json()
        nama_proyek = data.get('nama_proyek')
        deskripsi = data.get('deskripsi')
        gambar_proyek = data.get('gambar_proyek', '')

        if not nama_proyek:
            return jsonify({"status": "gagal", "pesan": "Nama proyek wajib diisi!"}), 400

        try:
            sql = "INSERT INTO proyek (nama_proyek, deskripsi, gambar_proyek) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nama_proyek, deskripsi, gambar_proyek))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Proyek berhasil disimpan!"}), 201
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()

# ==========================================
# 3 & 4. ROUTE UPDATE (PUT) & DELETE (DELETE)
# ==========================================
@projects_bp.route('/api/admin/projects/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_project(id):
    if not session.get('logged_in'):
        return jsonify({"status": "gagal", "pesan": "Akses ditolak"}), 401

    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "gagal", "pesan": "Database tidak terhubung"}), 500
    cursor = conn.cursor()

    # JALUR UPDATE DATA (PUT)
    if request.method == 'PUT':
        data = request.get_json()
        nama_proyek = data.get('nama_proyek')
        deskripsi = data.get('deskripsi')
        gambar_proyek = data.get('gambar_proyek')

        try:
            sql = "UPDATE proyek SET nama_proyek=%s, deskripsi=%s, gambar_proyek=%s WHERE id=%s"
            cursor.execute(sql, (nama_proyek, deskripsi, gambar_proyek, id))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Proyek berhasil diperbarui!"}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()

    # JALUR HAPUS DATA (DELETE)
    elif request.method == 'DELETE':
        try:
            sql = "DELETE FROM proyek WHERE id = %s"
            cursor.execute(sql, (id,))
            conn.commit()
            cursor.close()
            return jsonify({"status": "sukses", "pesan": "Proyek berhasil dihapus!"}), 200
        except Exception as e:
            return jsonify({"status": "gagal", "pesan": str(e)}), 500
        finally:
            conn.close()