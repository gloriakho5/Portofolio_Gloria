from flask import Blueprint, current_app

# Membuat Blueprint untuk halaman utama website sesuai instruksi asdos
utama_bp = Blueprint('utama', __name__)

@utama_bp.route('/')
def home():
    # Mengirimkan file index.html dari root ke browser pengunjung
    return current_app.send_static_file('index.html')