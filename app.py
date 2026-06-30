import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import resend

# --- 1. MUAT VARIABEL LINGKUNGAN DARI FILE .ENV ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# --- 2. FORCE SYSTEM PYTHON UNTUK MENEMUKAN FOLDER BACKEND ---
BACKEND_DIR = os.path.join(BASE_DIR, 'Backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from config import Config
from model import get_db_connection

# --- 3. IMPORT BLUEPRINT BACKEND ---
# --- 3. IMPORT BLUEPRINT BACKEND ---
# --- 3. IMPORT BLUEPRINT BACKEND ---
from Backend.admin.login import login_bp
from Backend.admin.dashboard import dashboard_bp
from Backend.admin.profiles import profiles_bp
from Backend.admin.skills import skills_bp
from Backend.admin.experience import experience_bp
from Backend.admin.projects import projects_bp
from Backend.admin.upload import upload_bp
from Backend.utama.utama import utama_bp 

# --- 4. INISIALISASI FLASK ---
app = Flask(__name__, static_folder='Frontend', static_url_path='')
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY", "gloria_default_key_123")
CORS(app)

# --- 5. REGISTER BLUEPRINT BACKEND API ---
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experience_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(utama_bp) 

# --- 6. RUTE ROUTING VIEW FRONTEND ---
@app.route('/admin/login')
def login_page():
    return app.send_static_file('admin/login.html')

@app.route('/admin/dashboard')
def dashboard_page():
    return app.send_static_file('admin/dashboard.html')

@app.route('/admin/profiles')
def profiles_page():
    return app.send_static_file('admin/profiles.html')

@app.route('/admin/skills')
def skills_page():
    return app.send_static_file('admin/skills.html')

@app.route('/admin/projects')
def projects_page():
    return app.send_static_file('admin/projects.html')

@app.route('/admin/experience')
def experience_page():
    return app.send_static_file('admin/experience.html')

# --- 7. ENDPOINT FORMULIR KONKAT (MURNI KIRIM EMAIL VIA RESEND API) ---
@app.route('/api/contact', methods=['POST'])
def send_contact_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "gagal", "pesan": "Payload data kosong"}), 400

        nama_pengirim = data.get('nama', 'Anonim')
        email_pengirim = data.get('email', 'tidak-ada-email@example.com')
        pesan = data.get('message', '')

        # Konfigurasi API Key Resend dari file .env
        resend.api_key = os.getenv("RESEND_API_KEY")
        
        if not resend.api_key:
            return jsonify({"status": "gagal", "pesan": "API Key Resend tidak ditemukan di .env"}), 500

        # KUNCI BIAR JADI: "from" harus menggunakan domain bawaan resend 'onboarding@resend.dev'
        # Dan "to" HARUS berupa email yang Anda gunakan saat mendaftar akun Resend tersebut.
        r = resend.Emails.send({
            "from": "Portfolio Contact <onboarding@resend.dev>",
            "to": "gloriakho5@gmail.com",  # <--- Ganti dengan email utama akun Resend Anda jika berbeda
            "subject": f"Pesan Portofolio Baru dari {nama_pengirim}",
            "html": f"""
                <h3>Ada Pesan Masuk dari Website Portofolio!</h3>
                <p><strong>Nama Pengirim:</strong> {nama_pengirim}</p>
                <p><strong>Email Pengirim:</strong> {email_pengirim}</p>
                <p><strong>Isi Pesan:</strong></p>
                <p style="background: #f4f4f5; padding: 10px; border-radius: 5px;">{pesan}</p>
            """
        })
        
        return jsonify({
            "status": "sukses", 
            "pesan": "Pesan berhasil dikirim! Silakan periksa kotak masuk (Inbox/Spam) Gmail Anda.",
            "id": r.get('id')
        }), 200

    except Exception as e:
        print(f"[Error Resend API]: {str(e)}")
        return jsonify({"status": "gagal", "pesan": str(e)}), 500

# --- BLOK UTAMA JALANNYA PROGRAM ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)