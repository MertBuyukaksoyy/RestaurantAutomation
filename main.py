from detector import detect_dishes
from utils import calculate_total

img_path = "static/sushi2.jpg"

detections = detect_dishes(img_path)
total, details = calculate_total(detections)

print(f"Toplam Hesap: {total} TL")
for d in details:
    print(f"- {d['item']} → {d['price']} TL")
