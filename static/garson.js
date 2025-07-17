async function fetchStatus() {
    const table = document.getElementById("tableSelect").value;
    const res = await fetch(`/get_table_status?table_id=${table}`);
    const data = await res.json();

    let html = `
        <p><strong>Siparişler:</strong></p>
        <ul>${data.orders.map(o => `<li>${o[0]} - ${o[1]}₺</li>`).join("")}</ul>
        <p><strong>Toplam:</strong> ${data.total} TL</p>
        <p><strong>Garson Bekleniyor:</strong> ${data.waiting_for_garson ? "Evet" : "Hayır"}</p>
        <p><strong>Garson Skorları:</strong></p>
        <ul>${Object.entries(data.garson_score).map(([g, s]) => `<li>${g}: ${s}</li>`).join("")}</ul>
    `;

    document.getElementById("status").innerHTML = html;
}

// Sayfa yüklendiğinde ve masa değiştiğinde durum getir
document.getElementById("tableSelect").addEventListener("change", fetchStatus);
window.onload = fetchStatus;

async function markGarsonArrived() {
    const table = document.getElementById("tableSelect").value;
    const garsonId = prompt("Garson ID gir:");
    if (!garsonId) return;

    await fetch("/garson_arrived", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table_id: table, garson_id: garsonId })
    });

    fetchStatus();
}

async function resetTable() {
    const table = document.getElementById("tableSelect").value;
    await fetch("/reset_table", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ table_id: table })
    });

    fetchStatus();
}
function loadHistory() {
    const tableId = localStorage.getItem("table_id") || "table_1"; // default table_1
    fetch(`/get_table_history?table_id=${tableId}`)
        .then(res => res.json())
        .then(data => {
            const historyDiv = document.getElementById("historyContent");
            historyDiv.innerHTML = "";

            if (data.length === 0) {
                historyDiv.innerHTML = "<p>Geçmiş sipariş yok.</p>";
            } else {
                data.forEach(entry => {
                    const div = document.createElement("div");
                    div.innerHTML = `
                        <strong>${entry.timestamp}</strong><br>
                        ${entry.orders.map(o => `${o[0]} - ₺${o[1]}`).join("<br>")}
                        <br><em>Toplam: ₺${entry.total}</em>
                        <br><small>Garson: ${entry.garson_id || "-"}</small>
                        <hr>
                    `;
                    historyDiv.appendChild(div);
                });
            }

            document.getElementById("historyModal").style.display = "block";
        });
}

