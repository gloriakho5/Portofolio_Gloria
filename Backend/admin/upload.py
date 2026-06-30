import os
from flask import Blueprint, request, jsonify
import cloudinary
import cloudinary.uploader

# 1. Inisialisasi Blueprint sesuai arsitektur asdos
upload_bp = Blueprint('upload', __name__)

# 2. Konfigurasi Kredensial Cloudinary secara otomatis dari file .env
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# 3. ENDPOINT UNTUK MENANGANI UGGHAAN BINARY GAMBAR (FIKS METHODS POST)
@upload_bp.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Memeriksa apakah ada file biner yang dikirim di dalam request formData
        if 'file' not in request.files:
            return jsonify({"status": "gagal", "pesan": "Tidak ada berkas file yang terdeteksi"}), 400
            
        file_to_upload = request.files['file']
        
        if file_to_upload.filename == '':
            return jsonify({"status": "gagal", "pesan": "Nama file tidak valid"}), 400

        # Melakukan proses upload langsung ke server Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            folder="portfolio_gloria" # Membuat folder otomatis di dashboard Cloudinary Anda
        )
        
        # Mengambil URL Secure (https) hasil unggahan Cloudinary
        file_url = upload_result.get('secure_url')
        
        # Mengembalikan response sukses berbentuk JSON untuk dibaca oleh JavaScript
        return jsonify({
            "status": "sukses",
            "pesan": "Berkas berhasil diunggah ke Cloudinary",
            "url": file_url
        }), 200

    except Exception as e:
        print(f"[Eror Blueprint Upload]: {str(e)}")
        return jsonify({"status": "gagal", "pesan": str(e)}), 500