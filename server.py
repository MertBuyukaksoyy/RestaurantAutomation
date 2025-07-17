from flask import Flask, request, jsonify, render_template
from state import TABLES, HISTORY
import json
import os
from detector import detect_dishes
from utils import calculate_total
from state import TABLES

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/guest_arrived", methods=["POST"])
def guest_arrived():
    table_id = request.json["table_id"]
    TABLES[table_id].mark_guest_arrived()
    return {"status": "ok", "message": "Müşteri geldi, garson bekleniyor."}

@app.route("/garson")
def garson_panel():
    return render_template("garson.html", tables=list(TABLES.keys()))


@app.route("/garson_arrived", methods=["POST"])
def garson_arrived():
    table_id = request.json["table_id"]
    garson_id = request.json["garson_id"]
    TABLES[table_id].garson_arrived(garson_id)
    return {"status": "ok", "message": f"Garson geldi, skor güncellendi."}

@app.route("/reset_table", methods=["POST"])
def reset_table():
    table_id = request.json["table_id"]
    t = TABLES[table_id]

    # Geçmişe yaz
    HISTORY[table_id].append(t.export_to_history())

    # Masayı sıfırla
    t.reset()

    return {"status": "ok", "message": f"{table_id} sıfırlandı ve geçmişe kaydedildi."}


@app.route("/get_table_status", methods=["GET"])
def get_table_status():
    table_id = request.args.get("table_id")
    t = TABLES[table_id]
    return jsonify({
        "orders": t.orders,
        "total": t.calculate_total(),
        "waiting_for_garson": t.waiting_for_garson,
        "garson_score": dict(t.garson_score)
    })

@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()
    table_id = data["table_id"]
    item_name = data["item"]
    item_price = data["price"]

    TABLES[table_id].add_item(item_name, item_price)
    return {"status": "ok", "message": f"{item_name} eklendi. Fiyat: {item_price}₺"}

@app.route("/get_all_status", methods=["GET"])
def get_all_status():
    return jsonify({
        table_id: {
            "orders": table.orders,
            "total": table.calculate_total(),
            "waiting_for_garson": table.waiting_for_garson,
            "garson_score": dict(table.garson_score)
        }
        for table_id, table in TABLES.items()
    })

@app.route("/get_table_history", methods=["GET"])
def get_table_history():
    table_id = request.args.get("table_id")
    return jsonify(HISTORY[table_id])

from flask import Flask, request, jsonify, render_template
from state import TABLES

@app.route("/menu")
def show_menu():
    table_id = request.args.get("table_id")
    if table_id not in TABLES:
        return "Geçersiz masa", 400

    TABLES[table_id].mark_guest_arrived()

    # price_list.json'dan menüyü oku
    with open("data/price_list.json", "r") as f:
        price_list = json.load(f)

    return render_template("menu.html", table_id=table_id, price_list=price_list)

@app.route("/camera")
def camera():
    return render_template("camera.html")

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    if "frame" not in request.files:
        return jsonify({"success": False, "error": "No image provided"})

    image_file = request.files["frame"]
    save_path = "static/uploaded.jpg"
    image_file.save(save_path)

    detections = detect_dishes(save_path)
    if not detections:
        return jsonify({"success": False, "message": "No detections"})

    # Table_1'e ekle
    for det in detections:
        TABLES["table_1"].add_item(det["item"], det["price"])

    return jsonify({"success": True, "details": detections})


if __name__ == "__main__":
    app.run(debug=True)
