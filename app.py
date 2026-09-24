import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# เก็บสถานะออเดอร์ที่กำลังเปิดอยู่ทั้งหมด
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
      active_orders[ticket] = data
      print(f"Active Order Updated [{action}]: Ticket {ticket}")

    elif action == "CLOSE":
      if ticket in active_orders:
        del active_orders[ticket]
        print(f"Active Order Removed [CLOSE]: Ticket {ticket}")

    elif action == "CLOSE_ALL":
      active_orders.clear()
      print("All Active Orders Cleared [CLOSE_ALL]")

    elif action == "SYNC":
      # --- ระบบ Auto-Purge / Snapshot Sync ---
      # Master ส่งรายชื่อ Ticket ทั้งหมดที่เปิดอยู่จริงมาเทียบ
      incoming_tickets = data.get("tickets", [])

      # หาตัวที่อยู่ใน active_orders แต่ไม่มีอยู่ในรายชื่อปัจจุบันของ Master -> ลบทิ้งทันที (Purge)
      current_active_keys = list(active_orders.keys())
      for t in current_active_keys:
        if t not in incoming_tickets:
          del active_orders[t]
          print(f"Auto-Purged Ghost Order: Ticket {t}")

    return jsonify({"status": "success"}), 200
  return jsonify({"status": "error"}), 400


@app.route("/get_active", methods=["GET"])
def get_active():
  return jsonify(list(active_orders.values())), 200


@app.route("/clear", methods=["GET", "POST"])
def clear_orders():
  global active_orders
  active_orders.clear()
  return (
      jsonify({
          "status": "success",
          "message": "All orders cleared from active list",
      }),
      200,
  )


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)