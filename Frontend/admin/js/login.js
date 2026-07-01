const API_URL = 'https://web-gloria-682024041-1f749.up.railway.app';
async function prosesLogin() {
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;

    if (!usernameInput || !passwordInput) {
        alert("Username dan password tidak boleh kosong!");
        return;
    }

    try {
        const respon = await fetch(`${API_URL}/api/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                username: usernameInput, 
                password: passwordInput 
            })
        });

        const hasil = await respon.json();

        if (hasil.status === 'sukses') {
            alert("Login Berhasil! Mengalihkan ke panel admin...");
            window.location.href = '/admin/dashboard';
        } else {
            alert("Gagal Login: " + hasil.pesan);
        }
    } catch (error) {
        console.error(error);
        alert("Gagal terhubung ke server backend Flask.");
    }
}