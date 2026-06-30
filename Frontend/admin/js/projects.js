// --- BERKAS JAVASCRIPT EKSTERNAL: projects.js ---

let idProyekTerpilih = null; // Penanda mode Tambah (null) atau Edit (ID)

// 1. FUNGSI UNTUK UPLOAD GAMBAR KE CLOUDINARY (DIPINDAHKAN DARI KODE HTML LAMA)
async function uploadGambarProyek() {
    const fileInput = document.getElementById('file-proyek');
    if (fileInput.files.length === 0) { alert('Pilih gambar proyek terlebih dahulu!'); return; }

    const btn = document.getElementById('btn-upload-project');
    btn.innerText = "Uploading...";
    btn.disabled = true;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const res = await fetch(`${API_URL}/api/upload`, { method: 'POST', body: formData });
        const hasil = await res.json();
        if (res.ok) {
            document.getElementById('input-url-proyek').value = hasil.url;
            alert('Gambar proyek berhasil tersimpan di Cloudinary!');
        } else {
            alert('Gagal: ' + hasil.pesan);
        }
    } catch (err) { 
        console.error(err); 
        alert('Gagal mengunggah file.'); 
    } finally { 
        btn.innerText = "Upload"; 
        btn.disabled = false; 
    }
}

// 2. FUNGSI READ: MEMUAT LIST PROYEK DARI DATABASE CLOUD TIDB
async function muatDaftarProjects() {
    try {
        const res = await fetch(`${API_URL}/api/admin/projects`);
        if (res.ok) {
            const json = await res.json();
            const container = document.getElementById('list-projects-admin');
            if (!container) return;

            if (json.data.length === 0) {
                container.innerHTML = `<p class="text-xs text-slate-400 pl-2">Belum ada karya proyek yang diunggah.</p>`;
                return;
            }

            container.innerHTML = json.data.map(p => `
                <div class="flex justify-between items-center bg-white p-4 rounded-xl border border-slate-200/60 shadow-2xs">
                    <div class="flex items-center gap-3 max-w-[70%]">
                        <div class="w-12 h-12 bg-slate-100 rounded-lg overflow-hidden border border-slate-200 flex-shrink-0">
                            ${p.gambar_proyek ? `<img src="${p.gambar_proyek}" class="w-full h-full object-cover">` : `<div class="w-full h-full flex items-center justify-center text-slate-300 text-xs">No Pic</div>`}
                        </div>
                        <div class="truncate">
                            <h4 class="font-bold text-slate-800 text-xs truncate">${p.nama_proyek}</h4>
                            <p class="text-[11px] text-slate-400 truncate">${p.deskripsi || 'Tidak ada deskripsi'}</p>
                        </div>
                    </div>
                    <div class="flex gap-1.5 flex-shrink-0">
                        <button onclick="isiFormUbahProyek(${JSON.stringify(p).replace(/"/g, '&quot;')})" class="px-2.5 py-1.5 bg-amber-500 text-white text-[10px] font-bold rounded-lg hover:bg-amber-600 cursor-pointer">Ubah</button>
                        <button onclick="hapusProyek(${p.id})" class="px-2.5 py-1.5 bg-red-600 text-white text-[10px] font-bold rounded-lg hover:bg-red-700 cursor-pointer">Hapus</button>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) { console.error(err); }
}

// 3. FUNGSI PRE-EDIT: MASUKKAN DATA LAMA KE INPUT FORM
function isiFormUbahProyek(p) {
    idProyekTerpilih = p.id;
    document.getElementById('input-nama-proyek').value = p.nama_proyek;
    document.getElementById('input-deskripsi-proyek').value = p.deskripsi || '';
    document.getElementById('input-url-proyek').value = p.gambar_proyek || '';

    document.getElementById('form-title-project').innerHTML = `<i class="fa-solid fa-pen-to-square text-amber-500"></i> Ubah Data Proyek`;
    const btn = document.getElementById('btn-simpan-project');
    btn.innerText = "Perbarui Karya Proyek";
    btn.className = "w-full py-3.5 bg-amber-500 text-white text-sm font-bold rounded-xl hover:bg-amber-600 shadow-md cursor-pointer";
}

// 4. FUNGSI ACTION: TAMBAH BARU (POST) / PERBARUI DATA (PUT) (KODE AWAL KAMU YANG DIUPDATE)
async function tambahProyek() {
    const urlGambar = document.getElementById('input-url-proyek').value;
    const payload = {
        nama_proyek: document.getElementById('input-nama-proyek').value,
        deskripsi: document.getElementById('input-deskripsi-proyek').value,
        gambar_proyek: urlGambar
    };

    if (!payload.nama_proyek) {
        alert('Nama proyek tidak boleh kosong!');
        return;
    }

    // Tentukan URL dan Metode dinamis berdasarkan status form (Tambah atau Edit)
    const url = idProyekTerpilih ? `${API_URL}/api/admin/projects/${idProyekTerpilih}` : `${API_URL}/api/admin/projects`;
    const metode = idProyekTerpilih ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: metode,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert(idProyekTerpilih ? 'Proyek sukses diperbarui!' : 'Proyek baru beserta gambar Cloudinary berhasil ditambahkan!');
            
            // Reset state form kembali bersih semula
            idProyekTerpilih = null;
            document.getElementById('input-nama-proyek').value = '';
            document.getElementById('input-tek-proyek').value = ''; 
            document.getElementById('input-deskripsi-proyek').value = '';
            document.getElementById('input-url-proyek').value = '';
            document.getElementById('file-proyek').value = '';

            document.getElementById('form-title-project').innerHTML = `<i class="fa-solid fa-folder-plus text-blue-500"></i> Tambah Proyek Baru`;
            const btn = document.getElementById('btn-simpan-project');
            btn.innerText = "Simpan Proyek Ke Cloud";
            btn.className = "w-full py-3.5 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 shadow-md transition-colors cursor-pointer";

            muatDaftarProjects(); // Memuat ulang list proyek aktif secara real-time
        } else {
            const errData = await res.json();
            alert('Gagal memproses proyek: ' + (errData.pesan || 'Eror internal server.'));
        }
    } catch (err) {
        console.error("Gagal menghubungi API:", err);
        alert('Terjadi kesalahan jaringan, pastikan server Flask app.py menyala.');
    }
}

// 5. FUNGSI ACTION: HAPUS DATA (DELETE)
async function hapusProyek(id) {
    if (confirm("Apakah Anda yakin ingin menghapus proyek ini? Tindakan ini akan langsung menghilangkannya dari halaman utama website.")) {
        try {
            const res = await fetch(`${API_URL}/api/admin/projects/${id}`, { method: 'DELETE' });
            if (res.ok) {
                alert('Proyek berhasil terhapus secara permanen!');
                muatDaftarProjects(); // Refresh tampilan UI Admin
            } else {
                alert('Gagal menghapus data.');
            }
        } catch (err) { console.error(err); }
    }
}
// Fungsi pembantu penangkap nama file untuk Dropzone Box
function tampilkanNamaFile(input) {
    const label = document.getElementById('nama-file-terpilih');
    if (input.files && input.files.length > 0) {
        label.innerText = `File terpilih: "${input.files[0].name}"`;
        label.classList.remove('text-slate-400', 'italic');
        label.classList.add('text-blue-600', 'font-semibold');
    } else {
        label.innerText = "Belum ada file yang dipilih (PNG, JPG, JPEG, WEBP)";
        label.classList.remove('text-blue-600', 'font-semibold');
        label.classList.add('text-slate-400', 'italic');
    }
}

// Jalankan otomatis muat list saat window siap
window.addEventListener('DOMContentLoaded', muatDaftarProjects);