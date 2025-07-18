import cv2
import requests
from collections import defaultdict, deque
from detector import detect_dishes
from utils import calculate_total

TABLE_ID = "table_1"

DETECTION_BUFFER = defaultdict(lambda: deque(maxlen=1))

CONFIRMED_ITEMS = set()

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    temp_path = "static/temp_frame.jpg"
    cv2.imwrite(temp_path, frame)

    detections = detect_dishes(temp_path, conf=0.5)
    total, details = calculate_total(detections)

    for det in details:
        x1, y1, x2, y2 = det["bbox"]
        cls = det["item"]
        price = det["price"]

        label = f"{cls} - {price}₺"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Bu nesne için eşsiz anahtar (sınıf + konum)
        key = f"{cls}_{x1}_{y1}_{x2}_{y2}"

        DETECTION_BUFFER[key].append(True)

        if key not in CONFIRMED_ITEMS and len(DETECTION_BUFFER[key]) == 1 and all(DETECTION_BUFFER[key]):
            try:
                # POST isteği ile sunucuya yemeği ekle
                requests.post("http://127.0.0.1:5000/add_item", json={
                    "table_id": TABLE_ID,
                    "item": cls,
                    "price": price
                })
                print(f"{cls} eklendi - {price}₺")
                CONFIRMED_ITEMS.add(key)
            except Exception as e:
                print("API'ye istek atılamadı:", e)

    cv2.putText(frame, f"Toplam: {total} TL", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Masa Goruntusu", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("r"):
        # Buffer'ları sıfırla
        DETECTION_BUFFER.clear()
        CONFIRMED_ITEMS.clear()
        print("Manuel olarak masa sıfırlandı.")

cap.release()
cv2.destroyAllWindows()
