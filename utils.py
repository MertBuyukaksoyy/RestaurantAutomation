import json
import requests
from state import TABLES


def add_detections_to_table(detections, table_id):
    for det in detections:
        cls_id = det["class_id"]
        cls_name = CLASS_NAMES[cls_id]
        price = PRICE_LIST.get(cls_name, 0)
        TABLES[table_id].add_item(cls_name, price)

def send_item_to_api(item_name, price, table_id="table_1"):
    url = "http://127.0.0.1:5000/add_item"
    data = {
        "table_id": table_id,
        "item": item_name,
        "price": price
    }
    try:
        response = requests.post(url, json=data)
        print("API'ye gönderildi:", response.json())
    except Exception as e:
        print("API hatası:", e)

with open("data/price_list.json", "r") as f:
    PRICE_LIST = json.load(f)

# class_id'den isme çevirme (YOLO names list)
with open("model/class_names.txt", "r") as f:
    CLASS_NAMES = [line.strip() for line in f]

def calculate_total(detections):
    total = 0
    details = []

    for det in detections:
        cls_name = CLASS_NAMES[det["class_id"]]
        price = PRICE_LIST.get(cls_name, 0)
        total += price
        details.append({
            "item": cls_name,
            "price": price,
            "bbox": det["bbox"]
        })

    return total, details
