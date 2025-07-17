from ultralytics import YOLO
import cv2
import json

# Modeli yükle
model = YOLO("model/best.pt")

# Sınıf isimlerini ve fiyatları JSON'dan yükle
with open("data/price_list.json", "r", encoding="utf-8") as f:
    CLASS_INFO = json.load(f)

# class_id'ye karşılık gelen class_name'i bul
ID_TO_NAME = {v["id"]: name for name, v in CLASS_INFO.items()}

# Tahmin fonksiyonu
def detect_dishes(image_path, conf=0.3):
    results = model.predict(source=image_path, conf=conf)
    detections = []

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf_score = float(box.conf[0])

            if cls_id in ID_TO_NAME:
                class_name = ID_TO_NAME[cls_id]
                price = CLASS_INFO[class_name]["price"]

                detections.append({
                    "item": class_name,
                    "price": price,
                    "confidence": float(conf_score),
                })
    return detections
