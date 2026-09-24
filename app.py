import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# เก็บสถานะออเดอร์ที่กำลังเปิดอยู่ทั้งหมด (Key คือ ticket)
active_orders = {}


@app.route("/", methods=["GET"])
def home():
  return "MAO Trade Copier State Server is Running!", 200


@app.route("/update", methods=["POST"])
def update_order():
  global active_orders
  data = request.get_json()
  if data:
    action = data.get("action")
    ticket = data.get("ticket")

    if action == "OPEN" or action == "MODIFY":
      # บันทึกหรืออัปเดตออเดอร์นี้ไว้ในรายการ Active
      active_orders[ticket] = data
      print(f"Active Order Updated [{action}]: Ticket {ticket}")

    elif action == "CLOSE":
      # ลบออกจากรายการ Active เมื่อมีการปิดไม้
      if ticket in active_orders:
        del active_orders[ticket]
        print(f"Active Order Removed [CLOSE]: Ticket {ticket}")

    elif action == "CLOSE_ALL":
      # ล้างทั้งหมดเมื่อปิดรวบ
      active_orders.clear()
      print("All Active Orders Cleared [CLOSE_ALL]")

    return jsonify({"status": "success"}), 200
  return jsonify({"status": "error"}), 400


@app.route("/get_active", methods=["GET"])
def get_active():
  # ส่งรายชื่อออเดอร์ที่กำลังเปิดอยู่ทั้งหมดกลับไปให้ Client ซิงค์
  return jsonify(list(active_orders.values())), 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)