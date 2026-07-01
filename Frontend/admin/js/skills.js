// Otomatis muat daftar keahlian dari database saat halaman selesai dimuat
document.addEventListener("DOMContentLoaded", () => {
    muatDaftarSkills();
});

// Fungsi Utama: Menambahkan keahlian baru ke database Flask + TiDB
async function tambahSkill() {
    const namaSkill = document.getElementById('input-skill').value;
    
    try {
        const res = await fetch(`${API_URL}/api/admin/skills`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nama_skill: namaSkill })
        });
        
        if (res.ok) {
            alert('Skill berhasil ditambahkan!');
            document.getElementById('input-skill').value = '';
            muatDaftarSkills(); // Memperbarui daftar di kanan secara instan
        } else {
            alert('Gagal menambahkan skill.');
        }
    } catch (error) {
        console.error("Eror saat menambah skill:", error);
    }
}

// Fungsi Utama: Menampilkan daftar keahlian dari database ke kontainer HTML
async function muatDaftarSkills() {
    const container = document.getElementById("container-skills-admin");
    if (!container) return;
    
    container.innerHTML = `<p class="text-xs text-zinc-400 italic pl-2">Memuat data...</p>`;

    try {
        // Mengambil data dari endpoint database kamu
        const respon = await fetch(`${API_URL}/api/admin/skills`);
        const data = await respon.json();

        container.innerHTML = ""; // Bersihkan teks memuat

        if (!data || data.length === 0) {
            container.innerHTML = `<p class="text-xs text-zinc-400 italic pl-2">Belum ada keahlian.</p>`;
            return;
        }

        // Jika data berbentuk objek pembungkus (misal: data.data), sesuaikan di bawah
        const listData = Array.isArray(data) ? data : (data.data || []);

        listData.forEach(item => {
            let iconClass = "fa-solid fa-code text-zinc-500"; 
            const namaKeahlian = item.nama_skill || item.name || "";
            const namaLower = namaKeahlian.toLowerCase();

            // Deteksi ikon otomatis agar visual mewah
            if (namaLower.includes("html")) iconClass = "fa-brands fa-html5 text-orange-500";
            else if (namaLower.includes("css")) iconClass = "fa-brands fa-css3-alt text-blue-500";
            else if (namaLower.includes("java") && !namaLower.includes("script")) iconClass = "fa-brands fa-java text-red-500";
            else if (namaLower.includes("javascript") || namaLower.includes("js")) iconClass = "fa-brands fa-js text-yellow-500";
            else if (namaLower.includes("python")) iconClass = "fa-brands fa-python text-sky-600";
            else if (namaLower.includes("react")) iconClass = "fa-brands fa-react text-cyan-400";
            else if (namaLower.includes("sql") || namaLower.includes("database")) iconClass = "fa-solid fa-database text-indigo-500";
            else if (namaLower.includes("tailwind")) iconClass = "fa-brands fa-tailwind text-teal-400";

            const cardHtml = `
                <div class="bg-white p-4 rounded-xl border border-pink-100/80 shadow-xs flex justify-between items-center hover:shadow-sm transition-all">
                    <div class="flex items-center space-x-3">
                        <i class="${iconClass} text-xl w-6 text-center"></i>
                        <span class="font-semibold text-sm text-zinc-700">${namaKeahlian}</span>
                    </div>
                    <button onclick="hapusSkill(${item.id})" class="px-3 py-1.5 bg-rose-600 text-white text-xs font-bold rounded-lg hover:bg-rose-700 transition cursor-pointer flex items-center gap-1">
                        <i class="fa-solid fa-trash text-[10px]"></i> Hapus
                    </button>
                </div>
            `;
            container.insertAdjacentHTML("beforeend", cardHtml);
        });
    } catch (error) {
        console.error("Gagal memuat:", error);
        container.innerHTML = `<p class="text-xs text-rose-500 italic pl-2">Gagal memuat data dari database.</p>`;
    }
}

// Fungsi Utama: Menghapus keahlian berdasarkan ID dari database
async function hapusSkill(id) {
    if (!confirm("Apakah Anda yakin ingin menghapus keahlian ini?")) return;

    try {
        const res = await fetch(`${API_URL}/api/admin/skills/${id}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            muatDaftarSkills(); // Refresh daftar live setelah sukses terhapus
        } else {
            alert("Gagal menghapus skill.");
        }
    } catch (error) {
        console.error("Eror saat menghapus:", error);
    }
}