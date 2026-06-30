// Mengatur efek aktif pada menu sidebar admin saat ini
document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll("div.w-64 a");
    links.forEach(link => {
        if(link.getAttribute("href") === currentPath) {
            link.classList.add("bg-blue-600", "text-white");
        }
    });
});