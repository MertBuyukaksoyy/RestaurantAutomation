# 🍽️ Akıllı Restoran Yemek Tanıma Sistemi

Bu proje, restoran masalarına yerleştirilmiş kameralar aracılığıyla masadaki yemekleri otomatik olarak tanıyan ve müşteri hesabına ekleyen bir sistemdir. Proje, yemeklerin tanınmasının yanı sıra garson müdahalelerini ve hesap sıfırlama işlemlerini de yönetir.

---

## 📸 Proje Özeti

- Kamera arayüzü, belirli aralıklarla masa görseli yakalayarak sunucuya gönderir.
- Sunucuda çalışan model, görsel üzerindeki yemekleri tespit eder ve JSON formatındaki fiyat listesine göre masaya otomatik olarak fiyatlandırma yapar.
- Garson paneli, hangi masada hangi yemeklerin tanındığını gösterir. Garson geldiğinde butonla onay verir ve hesap sıfırlanabilir.
- Müşteri, masadaki QR kodu okutarak ilgili masaya özel menüyü görüntüleyebilir.

---

## 🚀 Özellikler

- 🔍 YOLO tabanlı yemek tanıma modeli
- 🍛 Menüdeki yemekleri ve fiyatlarını JSON dosyasından alma
- 📷 Kamera arayüzü ile otomatik görsel gönderimi
- 🧾 Her masa için canlı hesap takibi
- 👨‍🍳 Garson paneli üzerinden hesap kontrol ve sıfırlama
- 🌐 Flask tabanlı web arayüz

---

## 📁 Proje Kurulumu

-Projeyi kurmak için bu repoyu indirdikten sonra pythonda gerekli kütüphaneler kurulur.
-Modelin eğitimi YOLOv8 ile colab ortamında yapılmıştır bu projede best.pt dosyası tahmin için kullanılmaktadır.
-Projeyi bilgisayarda çalıştırmak için server.py çalıştırılır sonrasında program çalıştığı localhost adresini verecekti o adrese gidilir.
-Proje çalıştırıldıktan sonra generate_qr.py çalıştırılır böylece masaların qrları proje dosya yolunda qrcodes klasörü altında oluşur ve bu qrlar masaya oturmak ve menüye ulaşmak için kullanılabilir.
-Sonrasında projenin çalıştığı adreste /garson endpointine giderek garson arayüzüne ulaşılabilir.
-Bilgisayardaki kamera ile tanıma yapılmak isteniyorsa /camera adresine gidilebilir.
-Eğer mobilde çalıştırılmak istenirse ngrok kullanılabilir.

