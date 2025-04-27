function initializeMap(x, y, name) {
    var map = L.map('map').setView([y, x], 13); // 使用缩放级别 13
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    L.marker([y, x]).addTo(map)
        .bindPopup(name)
        .openPopup();
}