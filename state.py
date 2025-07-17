from collections import defaultdict
import time
import threading

HISTORY = defaultdict(list)
class Table:
    def __init__(self, table_id):
        self.table_id = table_id
        self.orders = []  # [(item, price)]
        self.last_reset_time = time.time()
        self.guest_arrival_time = None
        self.waiting_for_garson = False
        self.garson_id = None
        self.garson_score = defaultdict(int)

    def add_item(self, item, price):
        self.orders.append((item, price))

    def calculate_total(self):
        return round(sum(p for _, p in self.orders), 2)

    def reset(self):
        # geçmişe kaydet
        HISTORY[self.table_id].append(self.export_to_history())

        self.orders = []
        self.guest_arrival_time = None
        self.waiting_for_garson = True
        self.garson_id = None

    def mark_guest_arrived(self):
        self.guest_arrival_time = time.time()
        self.waiting_for_garson = True

        # 60 saniyelik kontrol thread'i başlat
        def timeout_check():
            time.sleep(60)
            if self.waiting_for_garson:
                print(f"[UYARI] {self.table_id}: Garson 60 sn içinde gelmedi. Skor düşürüldü.")
                self.garson_score["geciken"] -= 1  # isimsiz düşüş kaydı
                self.waiting_for_garson = False  # tekrar düşmesin

        threading.Thread(target=timeout_check, daemon=True).start()

    def garson_arrived(self, garson_id):
        self.garson_id = garson_id
        delay = time.time() - self.guest_arrival_time
        if delay <= 60:
            self.garson_score[garson_id] += 1
        else:
            self.garson_score[garson_id] -= 1
        self.waiting_for_garson = False

    def export_to_history(self):
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "orders": self.orders.copy(),
            "total": self.calculate_total(),
            "garson_id": self.garson_id
        }

# Global olarak 2 masa tanımı
TABLES = {
    "table_1": Table("table_1"),
    "table_2": Table("table_2")
}
