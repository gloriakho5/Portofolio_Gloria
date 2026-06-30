async function loadDashboardStats() {
    const res = await fetch(`${API_URL}/api/dashboard/stats`);
    if (res.ok) {
        const data = await res.json();
        document.getElementById('stat-skills').innerText = data.skills;
        document.getElementById('stat-projects').innerText = data.projects;
    }
}
window.onload = loadDashboardStats;