async function tambahSkill() {
    const namaSkill = document.getElementById('input-skill').value;
    const res = await fetch(`${API_URL}/api/admin/skills`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nama_skill: namaSkill })
    });
    if (res.ok) {
        alert('Skill berhasil ditambahkan!');
        document.getElementById('input-skill').value = '';
    }
}