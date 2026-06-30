-- 1. Tabel Profil
CREATE TABLE IF NOT EXISTS profil (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    peran VARCHAR(100),
    bio TEXT,
    foto VARCHAR(255)  -- Untuk menyimpan URL gambar dari Cloudinary
);

-- 2. Tabel Skill
CREATE TABLE IF NOT EXISTS skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_skill VARCHAR(50) NOT NULL,
    tingkat VARCHAR(50)
);

-- 3. Tabel Pengalaman
CREATE TABLE IF NOT EXISTS pengalaman (
    id INT AUTO_INCREMENT PRIMARY KEY,
    posisi VARCHAR(100) NOT NULL,
    perusahaan VARCHAR(100) NOT NULL,
    tahun_mulai VARCHAR(10),
    tahun_selesai VARCHAR(10),
    deskripsi TEXT
);

-- 4. Tabel Proyek
CREATE TABLE IF NOT EXISTS proyek (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_proyek VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    link_proyek VARCHAR(255),
    gambar_proyek VARCHAR(255)  -- Untuk menyimpan URL gambar dari Cloudinary
);

-- 5. Tabel Kontak
CREATE TABLE IF NOT EXISTS kontak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pengirim VARCHAR(100) NOT NULL,
    email_pengirim VARCHAR(100) NOT NULL,
    pesan TEXT,
    tanggal_kirim TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabel Admin (Untuk Login)
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Masukkan akun admin default sesuai ketentuan tugas
INSERT INTO admin (username, password) 
VALUES ('admin', 'admin123')
ON DUPLICATE KEY UPDATE username=username;