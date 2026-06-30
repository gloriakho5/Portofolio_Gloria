from flask import Blueprint, jsonify
from model import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "gagal", "pesan": "Database gagal terhubung"}), 500
    
    try:
        cursor = conn.cursor()
        
        # Menggunakan 'AS total_skills' untuk mengunci nama kunci agar pasti terbaca oleh Python
        cursor.execute("SELECT COUNT(*) AS total_skills FROM skill")
        res_skills = cursor.fetchone()
        total_skills = res_skills['total_skills'] if res_skills else 0
        
        # Menggunakan 'AS total_projects' untuk mengunci nama kunci proyek
        cursor.execute("SELECT COUNT(*) AS total_projects FROM proyek")
        res_projects = cursor.fetchone()
        total_projects = res_projects['total_projects'] if res_projects else 0
        
        cursor.close()
        return jsonify({
            "skills": total_skills,
            "projects": total_projects
        }), 200
        
    except Exception as e:
        return jsonify({"status": "gagal", "pesan": str(e)}), 500
    finally:
        conn.close()