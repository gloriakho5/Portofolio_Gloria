// --- BERKAS JAVASCRIPT EKSTERNAL: experience.js ---

let idDataTerpilih = null; // Penanda mode update

// 1. FUNGSI PEMBANTU: REAL-TIME PREVIEWING LOKAL
function updateLivePreview() {
    const pt = document.getElementById('input-pt').value;
    const jabatan = document.getElementById('input-jabatan').value;
    const mulai = document.getElementById('input-mulai').value;
    const selesai = document.getElementById('input-selesai').value;
    const deskripsi = document.getElementById('input-deskripsi').value;

    document.getElementById('preview-pt').innerText = pt || "Nama Instansi / Perusahaan";
    document.getElementById('preview-jabatan').innerText = jabatan || "Nama Jabatan Muncul Di Sini";
    document.getElementById('preview-tahun').innerText = `${mulai || '2024'} - ${selesai || 'Sekarang'}`;
    document.getElementById('preview-deskripsi').innerText = deskripsi || "Isi deskripsi kegiatan, tanggung jawab...";
}

// 2. FUNGSI READ: AMBIL DATA LAMA DARI DATABASE UNTUK FITUR UBAH & HAPUS
async function muatDaftarExperience() {
    try {
        const res = await fetch('/api/experience');
        if (res.ok) {
            const data = await res.json();
            const container = document.getElementById('list-experience-admin');
            if (!container) return;

            if (data.length === 0) {
                container.innerHTML = `<p class="text-xs text-slate-400 pl-2">Belum ada riwayat pengalaman.</p>`;
                return;
            }

            container.innerHTML = data.map(e => `
                <div class="flex justify-between items-center bg-white p-4 rounded-xl border border-slate-200/70 shadow-2xs">
                    <div class="max-w-[65%]">
                        <h4 class="font-bold text-slate-800 text-xs truncate">${e.posisi}</h4>
                        <p class="text-[11px] text-blue-600 font-medium truncate">${e.perusahaan}</p>
                    </div>
                    <div class="flex gap-1.5">
                        <button onclick="isiFormUbah(${JSON.stringify(e).replace(/"/g, '&quot;')})" class="px-2.5 py-1.5 bg-amber-500 text-white text-[10px] font-bold rounded-lg hover:bg-amber-600 transition-colors cursor-pointer">Ubah</button>
                        <button onclick="hapusExperience(${e.id})" class="px-2.5 py-1.5 bg-red-600 text-white text-[10px] font-bold rounded-lg hover:bg-red-700 transition-colors cursor-pointer">Hapus</button>
                    </div>
                </div>
            `).join('');
        }
    } catch (err) { console.error(err); }
}

// 3. FUNGSI UPDATE PREPARATION: ISI KOTAK INPUT DENGAN DATA YANG INGIN DIUBAH
function isiFormUbah(e) {
    idDataTerpilih = e.id;
    document.getElementById('input-pt').value = e.perusahaan;
    document.getElementById('input-jabatan').value = e.posisi;
    document.getElementById('input-mulai').value = e.tahun_mulai || '';
    document.getElementById('input-selesai').value = e.tahun_selesai || '';
    document.getElementById('input-deskripsi').value = e.deskripsi || '';
    
    updateLivePreview();

    document.getElementById('form-title').innerHTML = `<i class="fa-solid fa-pen-to-square text-amber-500"></i> Ubah Data Pengalaman`;
    const btn = document.getElementById('btn-simpan-experience');
    btn.innerText = "Perbarui Data Pengalaman";
    btn.className = "w-full py-3.5 bg-amber-500 text-white text-sm font-bold rounded-xl hover:bg-amber-600 transition-all shadow-md cursor-pointer";
}

// 4. FUNGSI ACTION: SIMPAN BARU (POST) ATAU UPDATE (PUT)
async function tambahExperience() {
    const payload = {
        perusahaan: document.getElementById('input-pt').value,
        posisi: document.getElementById('input-jabatan').value,
        tahun_mulai: document.getElementById('input-mulai').value,
        tahun_selesai: document.getElementById('input-selesai').value,
        deskripsi: document.getElementById('input-deskripsi').value
    };

    if (!payload.perusahaan || !payload.posisi) {
        alert("Peringatan: Kolom Instansi dan Jabatan tidak boleh kosong!");
        return;
    }

    const url = idDataTerpilih ? `/api/experience/${idDataTerpilih}` : `/api/experience`;
    const metode = idDataTerpilih ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: metode,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (res.ok) {
            alert(idDataTerpilih ? 'Sukses memperbarui data!' : 'Sukses menambahkan data baru!');
            
            // Reset Keadaan
            idDataTerpilih = null;
            document.getElementById('input-pt').value = '';
            document.getElementById('input-jabatan').value = '';
            document.getElementById('input-mulai').value = '';
            document.getElementById('input-selesai').value = '';
            document.getElementById('input-deskripsi').value = '';
            
            document.getElementById('form-title').innerHTML = `<i class="fa-regular fa-square-plus text-blue-500"></i> Tambah Pengalaman Baru`;
            const btn = document.getElementById('btn-simpan-experience');
            btn.innerText = "Simpan Pengalaman Ke Cloud";
            btn.className = "w-full py-3.5 bg-blue-600 text-white text-sm font-bold rounded-xl hover:bg-blue-700 transition-all shadow-md cursor-pointer";
            
            updateLivePreview();
            muatDaftarExperience();
        } else {
            alert('Gagal memproses data.');
        }
    } catch (err) { console.error(err); }
}

// 5. FUNGSI ACTION: HAPUS DATA (DELETE)
async function hapusExperience(id) {
    if (confirm("Apakah Anda yakin ingin menghapus riwayat pengalaman ini?")) {
        try {
            const res = await fetch(`/api/experience/${id}`, { method: 'DELETE' });
            if (res.ok) {
                alert('Data berhasil dihapus dari cloud!');
                muatDaftarExperience();
            }
        } catch (err) { console.error(err); }
    }
}

// Jalankan otomatis saat halaman termuat
window.onload = () => {
    muatDaftarExperience();
};