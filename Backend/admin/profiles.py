from flask import Blueprint, request, jsonify
from model import get_db_connection

profiles_bp = Blueprint('profiles', __name__)

@profiles_bp.route('/api/profile', methods=['GET', 'POST'])
def manage_profile():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM profil LIMIT 1")
        profile = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(profile or {})
        
    elif request.method == 'POST':
        data = request.json
        nama = data.get('nama')
        peran = data.get('peran')
        bio = data.get('bio')
        foto = data.get('foto')
        
        cursor.execute("SELECT id FROM profil LIMIT 1")
        exist = cursor.fetchone()
        
        if exist:
            cursor.execute(
                "UPDATE profil SET nama=%s, peran=%s, bio=%s, foto=%s WHERE id=%s",
                (nama, peran, bio, foto, exist['id'])
            )
        else:
            cursor.execute(
                "INSERT INTO profil (nama, peran, bio, foto) VALUES (%s, %s, %s, %s)",
                (nama, peran, bio, foto)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "sukses"})