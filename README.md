# Mini-HDFS: Distributed Storage & Fault Tolerance Simulation

Hệ thống lưu trữ phân tán mô phỏng Apache Hadoop HDFS (Mini-HDFS) được xây dựng bằng Python/Flask và triển khai trên mạng LAN ảo P2P ZeroTier.

---

## 🌟 Tính năng cốt lõi (Core Features)

1. **Kiến trúc Master - Worker (NameNode & DataNodes):**
   - **NameNode (Master - Cổng 5000):** Quản lý metadata, ánh xạ file ra các khối và điều phối replication.
   - **DataNodes (Workers - Cổng 6000/6001):** Lưu trữ các block vật lý, phục vụ đọc/ghi block và gửi Heartbeat định kỳ.
2. **Phân khối & Nhân bản (Block-level Splitting & Replication):**
   - Kích thước khối (Block size): `500 KB`.
   - Hệ số nhân bản (Replication Factor): `2` (Mỗi block được lưu độc lập trên 2 máy khác nhau).
3. **Cơ chế nhịp tim (Heartbeat Keepalive):**
   - DataNodes gửi nhịp tim định kỳ mỗi 5 giây (`/heartbeat`) để Master giám sát trạng thái `ONLINE`/`OFFLINE`.
4. **Kiểm soát toàn vẹn dữ liệu (SHA-256 Data Integrity):**
   - Băm SHA-256 từng block và toàn bộ file gốc, tự động đối soát khi ghép file.
5. **Khả năng chịu lỗi & Khôi phục P2P (Fault Tolerance & Self-Healing):**
   - Nếu 1 DataNode rớt mạng, Master tự động Failover sang bản sao dự phòng.
   - **Đặc biệt:** Ngay cả khi Master sập hoàn toàn, các Worker Nodes có thể chạy script `pull_and_merge.py` qua mạng ZeroTier để tự động kéo các block còn thiếu từ máy bạn bè về và ghép lại video hoàn chỉnh!
6. **Giao diện Web trực quan (Web Dashboard):**
   - Giám sát cụm, tải file lên (Upload), tải xuống (Download), xem Metadata và xóa file.

---

## 📁 Cấu trúc thư mục

```text
bigdata/
├── mini-hdfs/
│   ├── storage/                 # Thư mục lưu các block trên máy trạm
│   │   ├── node_master/
│   │   ├── node1/
│   │   ├── node2/
│   │   └── node3/
│   ├── templates/
│   │   └── index.html           # Giao diện Web Dashboard quản trị cụm
│   ├── app.py                   # NameNode Master & Web Server (Port 5000)
│   ├── datanode_master.py       # DataNode Worker (Port 6001)
│   ├── pull_and_merge.py        # Script khôi phục P2P khi Master gặp sự cố
│   └── metadata.json            # Siêu dữ liệu lưu trữ ánh xạ block & hash
├── sample_demo.txt              # File mẫu thử nghiệm
└── README.md
```

---

## 🚀 Hướng dẫn cài đặt và khởi chạy

### 1. Cài đặt thư viện phụ thuộc
```bash
python -m venv venv
# Trên Windows:
.\venv\Scripts\Activate.ps1
# Trên Linux/Mac:
source venv/bin/activate

pip install flask requests werkzeug python-docx
```

### 2. Cấu hình IP ZeroTier trong `mini-hdfs/app.py`
```python
DATANODES = {
    "node_master_my_pc": "http://127.0.0.1:6001",   
    "node_ducanh": "http://10.122.174.174:6000",
    "node_khanhphong": "http://10.122.174.211:6000"
}
```

### 3. Khởi chạy cụm Mini-HDFS
- **Tại máy Master:**
  ```bash
  cd mini-hdfs
  python app.py            # Chạy Master trên cổng 5000
  python datanode_master.py # Chạy Worker 1 trên cổng 6001
  ```
- **Tại máy Worker thành viên:**
  ```bash
  python datanode_worker.py # Chạy Worker 2/3 trên cổng 6000
  ```

### 4. Truy cập Web Dashboard
Mở trình duyệt: `http://localhost:5000`

---

## 🛠️ Kịch bản Demo Chịu lỗi P2P khi Master sập
Khi máy chủ Master bị tắt:
1. Mở máy thành viên (máy Phong hoặc Đức Anh).
2. Chạy script khôi phục:
   ```bash
   python pull_and_merge.py
   ```
3. Script tự động phát hiện các block còn thiếu, kéo từ máy đối tác qua ZeroTier API `/get_block/...` và ghép lại thành `video_hoanchinh.mp4` đầy đủ 100%!
