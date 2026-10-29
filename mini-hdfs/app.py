import hashlib
import io
import json
import os
import random
from pathlib import Path
import requests  
from flask import Flask, jsonify, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
METADATA_FILE = BASE_DIR / "metadata.json"

# ==================== BƯỚC 2: CẤU HÌNH DATANODES QUA ZEROTIER ====================
# Thay các IP 10.147.17.x dưới đây bằng IP ZeroTier thực tế của bạn và các bạn của bạn
DATANODES = {
    "node_master_my_pc": "http://127.0.0.1:6001",   
    "node_ducanh": "http://10.122.174.174:6000",
    "node_khanhphong": "http://10.122.174.211:6000"
}

NODES = list(DATANODES.keys())

# Dùng 500 KB để file nhỏ cũng chia thành nhiều block
BLOCK_SIZE = 500 * 1024
REPLICATION_FACTOR = 2

# Quản lý trạng thái Online/Offline của từng Node
NODE_STATUS = {node: "OFFLINE" for node in NODES}

def initialize_system() -> None:
    if not METADATA_FILE.exists():
        save_metadata({})

def load_metadata() -> dict:
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_metadata(metadata: dict) -> None:
    temp_file = METADATA_FILE.with_suffix(".tmp")
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)
    temp_file.replace(METADATA_FILE)

def calculate_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# ==================== CẬP NHẬT: XỬ LÝ HEARTBEAT & KIỂM TRA NODE ====================
@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    """Lắng nghe nhịp tim từ các DataNodes gửi về"""
    data = request.json or {}
    node_name = data.get("node_name")
    if node_name in NODE_STATUS:
        NODE_STATUS[node_name] = "ONLINE"
    return jsonify({"status": "acknowledged"}), 200

def node_is_available(node: str) -> bool:
    """Kiểm tra Node có đang ONLINE hay không qua trạng thái Heartbeat"""
    return NODE_STATUS.get(node) == "ONLINE"

def choose_nodes_for_replication() -> list[str]:
    available_nodes = [node for node in NODES if node_is_available(node)]
    if len(available_nodes) < REPLICATION_FACTOR:
        raise RuntimeError(f"At least {REPLICATION_FACTOR} available nodes are required.")
    return random.sample(available_nodes, REPLICATION_FACTOR)

def delete_old_blocks(filename: str, file_metadata: dict) -> None:
    """Xóa block trên các máy DataNode từ xa"""
    for block in file_metadata.get("blocks", []):
        block_name = block["block_name"]
        for node in block.get("nodes", []):
            if node in DATANODES:
                node_url = DATANODES[node]
                try:
                    requests.delete(f"{node_url}/delete_block/{block_name}", timeout=2)
                except Exception:
                    pass

@app.route("/")
def index():
    metadata = load_metadata()
    node_status = {node: node_is_available(node) for node in NODES}
    return render_template(
        "index.html",
        files=metadata,
        node_status=node_status,
        block_size=BLOCK_SIZE,
        replication_factor=REPLICATION_FACTOR
    )

# ==================== CẬP NHẬT: UPLOAD FILE SANG DATANODE QUA HTTP ====================
@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        return "No file selected.", 400
    filename = secure_filename(uploaded_file.filename)
    if not filename:
        return "Invalid filename.", 400
    file_data = uploaded_file.read()
    if len(file_data) == 0:
        return "The selected file is empty.", 400
    metadata = load_metadata()
    if filename in metadata:
        delete_old_blocks(filename, metadata[filename])
    blocks = []
    try:
        for block_index, start in enumerate(range(0, len(file_data), BLOCK_SIZE)):
            block_data = file_data[start:start + BLOCK_SIZE]
            block_name = f"{filename}.block_{block_index:04d}"
            selected_nodes = choose_nodes_for_replication()
            
            # Gửi block dữ liệu qua mạng HTTP POST tới các DataNode được chọn
            for node in selected_nodes:
                node_url = DATANODES[node]
                response = requests.post(
                    f"{node_url}/upload_block",
                    data={"block_name": block_name},
                    files={"file": (block_name, block_data)},
                    timeout=60
                )
                if response.status_code != 200:
                    raise RuntimeError(f"Failed to upload block {block_name} to {node}")

            blocks.append({
                "index": block_index,
                "block_name": block_name,
                "size": len(block_data),
                "hash": calculate_hash(block_data),
                "nodes": selected_nodes
            })
    except Exception as error:
        return f"Upload failed: {error}", 500
    metadata[filename] = {
        "original_filename": filename,
        "file_size": len(file_data),
        "file_hash": calculate_hash(file_data),
        "number_of_blocks": len(blocks),
        "replication_factor": REPLICATION_FACTOR,
        "blocks": blocks
    }
    save_metadata(metadata)
    return redirect(url_for("index"))

# ==================== CẬP NHẬT: DOWNLOAD FILE TỪ DATANODE QUA HTTP ====================
@app.route("/download/<filename>")
def download(filename: str):
    metadata = load_metadata()
    file_metadata = metadata.get(filename)
    if file_metadata is None:
        return "File not found in metadata.", 404
    reconstructed_file = bytearray()
    sorted_blocks = sorted(file_metadata["blocks"], key=lambda block: block["index"])
    for block in sorted_blocks:
        block_data = None
        selected_replica = None
        for node in block["nodes"]:
            if not node_is_available(node):
                continue
            
            # Tải block từ DataNode qua mạng HTTP GET
            node_url = DATANODES[node]
            try:
                resp = requests.get(f"{node_url}/get_block/{block['block_name']}", timeout=5)
                if resp.status_code == 200:
                    candidate_data = resp.content
                    if calculate_hash(candidate_data) == block["hash"]:
                        block_data = candidate_data
                        selected_replica = node
                        break
            except Exception:
                continue

        if block_data is None:
            return f"Cannot recover {block['block_name']}. All replicas are missing or corrupted.", 500
        reconstructed_file.extend(block_data)
    reconstructed_hash = calculate_hash(bytes(reconstructed_file))
    if reconstructed_hash != file_metadata["file_hash"]:
        return "File integrity check failed.", 500
    return send_file(
        io.BytesIO(reconstructed_file),
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream"
    )

@app.route("/metadata/<filename>")
def view_file_metadata(filename: str):
    metadata = load_metadata()
    file_metadata = metadata.get(filename)
    if file_metadata is None:
        return jsonify({"error": "File not found"}), 404
    return jsonify(file_metadata)

@app.route("/cluster")
def cluster_status():
    result = {}
    for node in NODES:
        available = node_is_available(node)
        result[node] = {
            "available": available,
            "status": "ONLINE" if available else "OFFLINE"
        }
    return jsonify(result)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename: str):
    metadata = load_metadata()
    file_metadata = metadata.get(filename)
    if file_metadata is None:
        return "File not found.", 404
    delete_old_blocks(filename, file_metadata)
    del metadata[filename]
    save_metadata(metadata)
    return f"Deleted {filename} and its block replicas."

if __name__ == "__main__":
    initialize_system()
    app.run(host="0.0.0.0", port=5000, debug=True)