import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# ตัวแปรกลางสำหรับเก็บสถานะออเดอร์ล่าสุด
latest_signal = {
    "action": "NONE",
    "ticket": 0,
    "symbol": "",
    "type": 0,
    "volume": 0.0,
    "price": 0.0,
    "balance": 0.0,
}


@app.route("/", methods=["GET"])
def home():
  return "MAO Trade Copier Server is Running!", 200


@app.route("/update", methods=["POST"])
def update_order():
  global latest_signal
  data = request.get_json()
  if data:
    latest_signal = data
    print(f"Received Signal: {latest_signal}")
    return jsonify({"status": "success", "message": "Signal updated"}), 200
  return jsonify({"status": "error", "message": "Invalid data"}), 400


@app.route("/get_latest", methods=["GET"])
def get_order():
  return jsonify(latest_signal), 200


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)