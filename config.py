import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TIDB_HOST = os.getenv('TIDB_HOST')
    TIDB_PORT = int(os.getenv('TIDB_PORT', 4000))
    TIDB_USER = os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TIDB_PASSWORD')
    TIDB_DATABASE = os.getenv('TIDB_DATABASE', 'test')
    SECRET_KEY = os.getenv('SECRET_KEY', 'p4ndu4n_tug4s_p0rtf0li0_r4h4si4')
    
    # Tambahan Konfigurasi untuk Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')