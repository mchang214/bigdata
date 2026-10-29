import os
import requests
import threading
import time
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

# Cấu hình kết nối
MASTER_IP = "127.0.0.1" 
MASTER_PORT = 5000
NODE_NAME = "node_master_my_pc"
STORAGE_DIR = "./storage/node_master"

os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/upload_block', methods=['POST'])
def upload_block():
    block_name = request.form.get('block_name')
    file = request.files['file']
    save_path = os.path.join(STORAGE_DIR, block_name)
    file.save(save_path)
    return jsonify({"status": "success", "message": f"Block {block_name} saved"}), 200

@app.route('/get_block/<block_name>', methods=['GET'])
def get_block(block_name):
    file_path = os.path.join(STORAGE_DIR, block_name)
    if os.path.exists(file_path):
        return send_file(file_path)
    return jsonify({"error": "Block not found"}), 404

def send_heartbeat():
    while True:
        try:
            requests.post(f"http://{MASTER_IP}:{MASTER_PORT}/heartbeat", json={
                "node_name": NODE_NAME,
                "status": "ONLINE"
            }, timeout=3)
        except Exception:
            pass
        time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=send_heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=6001)