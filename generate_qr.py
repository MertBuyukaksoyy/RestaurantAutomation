import qrcode

def create_qr_for_table(table_id):
    # Menü ve bildirim için açılacak URL
    url = f"   https://eb66a68527e3.ngrok-free.app/menu?table_id={table_id}"

    # QR kod oluştur
    img = qrcode.make(url)
    img.save(f"qrcodes/{table_id}.png")
    print(f"{table_id} için QR kodu oluşturuldu.")

# Örnek: 2 masa için
if __name__ == "__main__":
    import os
    os.makedirs("qrcodes", exist_ok=True)
    for i in range(1, 3):
        create_qr_for_table(f"table_{i}")
