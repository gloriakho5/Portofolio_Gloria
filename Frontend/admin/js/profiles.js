async function simpanProfil() {
    const payload = {
        nama: document.getElementById('input-nama').value,
        peran: document.getElementById('input-peran').value,
        bio: document.getElementById('input-bio').value,
        foto: document.getElementById('input-url-foto').value
    };
    const res = await fetch(`${API_URL}/api/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    if (res.ok) alert('Profil sukses diperbarui!');
}