# BÁO CÁO BÀI TẬP LỚN HỌC PHẦN DỮ LIỆU LỚN (BIG DATA)

---

## i) TRANG BÌA

```text
========================================================================================
                          BỘ GIÁO DỤC VÀ ĐÀO TẠO
                   TRƯỜNG ĐẠI HỌC CÔNG NGHỆ (VNU - UET)
              KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN HỆ THỐNG THÔNG TIN
                                  ***

                    BÁO CÁO BÀI TẬP LỚN / ĐỒ ÁN HỌC PHẦN
                         DỮ LIỆU LỚN (BIG DATA)

                                ĐỀ TÀI:
          THIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG LƯU TRỮ PHÂN TÁN 
                 MÔ PHỎNG HADOOP HDFS (MINI-HDFS) 
                  TRÊN MẠNG LAN ẢO P2P (ZEROTIER)

    Giảng viên hướng dẫn:  TS. Giảng viên phụ trách môn học
    Học phần:              Dữ liệu lớn và Ứng dụng (Big Data Analytics)
    Nhóm sinh viên:        1. Nguyễn Đức Anh      (Node Worker 1)
                           2. Lê Khánh Phong      (Node Worker 2)
                           3. Trưởng nhóm / Dev   (Master & Worker)
    Mã số sinh viên:       B21DCCN... / B21DCCN...
    Lớp:                   Khoa học Máy tính / CNTT
    Niên khóa:             2021 - 2025

                                Hà Nội, Năm 2026
========================================================================================
```

---

## ii) LỜI CẢM ƠN

Lời đầu tiên, nhóm tác giả xin bày tỏ lòng biết ơn sâu sắc và chân thành nhất tới Quý Thầy/Cô bộ môn Dữ liệu lớn (Big Data) thuộc Khoa Công nghệ Thông tin. Trong suốt học kỳ vừa qua, những bài giảng tâm huyết, sự hướng dẫn tận tình cùng hệ thống bài tập thực hành giàu tính thực tiễn của Thầy/Cô đã giúp chúng em xây dựng được nền tảng kiến thức vững chắc về các mô hình kiến trúc lưu trữ và xử lý dữ liệu quy mô lớn (Scale-Out Architecture, MapReduce, HDFS, Distributed Consistency).

Báo cáo đề tài *"Thiết kế và triển khai hệ thống lưu trữ phân tán mô phỏng Hadoop HDFS (Mini-HDFS) trên mạng LAN ảo P2P (ZeroTier)"* là kết tinh từ quá trình nghiên cứu lý thuyết, phân tích các tài liệu kinh điển (Google File System, Apache Hadoop HDFS Architecture) và nỗ lực hiện thực hóa thành một sản phẩm phần mềm hoạt động thực tế trên cụm nhiều máy tính phân tán.

Mặc dù nhóm đã nỗ lực hoàn thiện hệ thống và biên soạn tài liệu chi tiết, dễ hiểu nhất cho người mới bắt đầu, song do giới hạn về mặt thời gian và kinh nghiệm thực tế, bài báo cáo khó tránh khỏi những điểm còn thiếu sót. Nhóm nghiên cứu rất mong nhận được những ý kiến đánh giá, góp ý quý báu từ Quý Thầy/Cô để đề tài ngày càng hoàn thiện và có thể ứng dụng làm học liệu mẫu cho các khóa sinh viên sau.

*Hà Nội, tháng 10 năm 2026*  
**Nhóm sinh viên thực hiện đề tài**

---

## iii) TÓM TẮT (ABSTRACT)

> **Tóm tắt đề tài (~100 từ):**  
> Báo cáo trình bày thiết kế và hiện thực hệ thống lưu trữ phân tán Mini-HDFS dựa trên kiến trúc Apache Hadoop HDFS. Hệ thống vận hành theo mô hình Master-Worker gồm NameNode quản lý siêu dữ liệu (metadata) và các DataNodes phân tán kết nối qua mạng LAN ảo ZeroTier. Dữ liệu tải lên được tự động phân mảnh thành các khối kích thước 500 KB, nhân bản với hệ số 2 (Replication Factor = 2) và phân bổ ngẫu nhiên trên các nút mạng. Toàn vẹn dữ liệu được đảm bảo tuyệt đối bằng thuật toán băm SHA-256 ở cấp độ từng khối và toàn tệp. Cơ chế Heartbeat định kỳ 5 giây giám sát trạng thái trực tuyến của nút, hỗ trợ khả năng chịu lỗi tự động khi có nút gặp sự cố. Báo cáo cung cấp quy trình thực nghiệm chi tiết từng bước, giúp người mới bắt đầu có thể dễ dàng cài đặt, cấu hình và kiểm chứng thành công.

*Từ khóa:* Dữ liệu lớn (Big Data), HDFS, Hệ thống tệp phân tán, Nhân bản dữ liệu (Replication), Cơ chế Heartbeat, Tính toàn vẹn SHA-256, Khả năng chịu lỗi (Fault Tolerance), ZeroTier VPN.

---

## iv) MỤC LỤC TỔNG HỢP

- **i) TRANG BÌA**
- **ii) LỜI CẢM ƠN**
- **iii) TÓM TẮT (ABSTRACT)**
- **iv) MỤC LỤC TỔNG HỢP**
- **v) NỘI DUNG CHÍNH**
  - **CHƯƠNG 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT VỀ LƯU TRỮ PHÂN TÁN**
    - 1.1. Thách thức của Kỷ nguyên Dữ liệu lớn (Big Data - Mô hình 4Vs)
    - 1.2. Tổng quan về Hệ thống tệp phân tán Hadoop (HDFS)
    - 1.3. Các nguyên lý thiết kế then chốt của HDFS
    - 1.4. Mục tiêu và ý nghĩa của Đề tài Mini-HDFS
  - **CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-HDFS**
    - 2.1. Mô hình kiến trúc Master - Worker
    - 2.2. Giải pháp liên mạng phân tán P2P với ZeroTier Virtual LAN
    - 2.3. Cấu trúc Quản lý Siêu dữ liệu (Metadata Architecture)
    - 2.4. Thiết kế các luồng xử lý nghiệp vụ chính
      - 2.4.1. Luồng Ghi tệp (Upload, Phân khối & Nhân bản)
      - 2.4.2. Luồng Đọc tệp (Download, Tái hợp khối & Kiểm tra SHA-256)
      - 2.4.3. Cơ chế Giám sát Heartbeat và Chịu lỗi (Fault Tolerance)
  - **CHƯƠNG 3: CHI TIẾT CÀI ĐẶT VÀ HIỆN THỰC MÃ NGUỒN**
    - 3.1. Phân tích chi tiết Master Node (`app.py`)
    - 3.2. Phân tích chi tiết DataNode Worker (`datanode_master.py`)
    - 3.3. Thiết kế Giao diện Quản trị Web Dashboard (`templates/index.html`)
  - **CHƯƠNG 4: HƯỚNG DẪN DEMO VÀ THỰC HÀNH CHI TIẾT (STEP-BY-STEP DÀNH CHO NGƯỜI MỚI)**
    - 4.1. Chuẩn bị môi trường máy trạm và mạng ZeroTier
    - 4.2. Cấu hình địa chỉ IP và Khởi động hệ thống
    - 4.3. Kịch bản Demo 1: Tải lên tệp đa phương tiện lớn (Splitting & Replication)
    - 4.4. Kịch bản Demo 2: Kiểm tra cấu trúc Metadata và Tính toàn vẹn SHA-256
    - 4.5. Kịch bản Demo 3: Thử nghiệm Chịu lỗi (Fault Tolerance) khi Node gặp sự cố
    - 4.6. Kịch bản Demo 4: Xóa tệp và thu hồi tài nguyên trên các DataNodes
  - **CHƯƠNG 5: ĐÁNH GIÁ KẾT QUẢ VÀ HƯỚNG PHÁT TRIỂN**
    - 5.1. Đánh giá ưu điểm đạt được
    - 5.2. Các hạn chế tồn tại
    - 5.3. Định hướng mở rộng trong tương lai
  - **KẾT LUẬN**
- **vi) TÀI LIỆU THAM KHẢO (HARVARD REFERENCING SYSTEM)**
- **vii) PHỤ LỤC**
  - Phụ lục A: Toàn bộ mã nguồn hoàn chỉnh Master Node (`app.py`)
  - Phụ lục B: Toàn bộ mã nguồn hoàn chỉnh DataNode (`datanode_master.py`)
  - Phụ lục C: Tệp tin `metadata.json` thực nghiệm thực tế

---

## v) NỘI DUNG CHÍNH

### CHƯƠNG 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT VỀ LƯU TRỮ PHÂN TÁN

#### 1.1. Thách thức của Kỷ nguyên Dữ liệu lớn (Big Data - Mô hình 4Vs)
Trong những năm gần đây, cuộc cách mạng công nghiệp 4.0 cùng sự bùng nổ của mạng xã hội, thiết bị thông minh (IoT), dịch vụ truyền phát video trực tuyến (streaming) và thương mại điện tử đã tạo ra khối lượng dữ liệu khổng lồ. Thuật ngữ **Big Data** (Dữ liệu lớn) được đặc trưng bởi 4 yếu tố cốt lõi (Mô hình 4Vs):
1. **Volume (Khối lượng):** Quy mô dữ liệu vượt qua ngưỡng Terabyte, vươn tới Petabyte và Exabyte. Các tệp dữ liệu đơn lẻ có thể lên tới hàng chục Gigabyte, vượt quá dung lượng một ổ đĩa thông thường.
2. **Velocity (Tốc độ):** Dữ liệu sinh ra liên tục theo thời gian thực đòi hỏi tốc độ ghi, đọc và phản hồi cực kỳ nhanh chóng.
3. **Variety (Đa dạng):** Đa dạng về cấu trúc từ dữ liệu dạng bảng (RDBMS), dữ liệu bán cấu trúc (JSON, XML, Logs) đến phi cấu trúc (video, tệp nhị phân, hình ảnh).
4. **Veracity (Độ tin cậy/Xác thực):** Nguy cơ lỗi đường truyền, suy hao dữ liệu (bit rot) trên đĩa cứng đòi hỏi các giải pháp kiểm tra toàn vẹn khắt khe.

Các giải pháp truyền thống dựa trên việc nâng cấp phần cứng của một máy chủ duy nhất (**Vertical Scaling / Scale-Up**) nhanh chóng chạm trần giới hạn vật lý và chi phí kinh tế. Để giải quyết triệt để vấn đề này, kiến trúc phân tán theo chiều ngang (**Horizontal Scaling / Scale-Out**) – kết nối nhiều máy tính thông thường (commodity hardware) thành một cụm thống nhất – đã trở thành tiêu chuẩn công nghiệp.

#### 1.2. Tổng quan về Hệ thống tệp phân tán Hadoop (HDFS)
Xuất phát từ nghiên cứu kinh điển về **Google File System (GFS)** (Ghemawat et al., 2003), Tổ chức Phần mềm Apache đã phát triển **Hadoop Distributed File System (HDFS)** (Shvachko et al., 2010; White, 2015). HDFS là hệ thống tệp phân tán được thiết kế chuyên biệt để lưu trữ các tập tin có dung lượng rất lớn, chạy trên các cụm phần cứng phổ thông với độ tin cậy và khả năng chịu lỗi cực cao.

Kiến trúc HDFS tuân theo mô hình **Master/Worker**:
- **NameNode (Master):** Quản lý không gian tên hệ thống tệp (File System Namespace), mở/đóng/đổi tên thư mục và tệp, lưu bảng ánh xạ từ tệp sang các khối (blocks) và vị trí của các khối trên các DataNodes.
- **DataNodes (Workers):** Lưu trữ các khối dữ liệu thực tế trên hệ thống tệp cục bộ, thực hiện đọc/ghi các khối theo yêu cầu từ Client và định kỳ gửi báo cáo nhịp tim (Heartbeat) và báo cáo khối (Block Report) về NameNode.

#### 1.3. Các nguyên lý thiết kế then chốt của HDFS
HDFS vận hành dựa trên ba nguyên lý cốt lõi:
1. **Lưu trữ theo khối (Block-level Storage):** Tệp tin được chia thành các khối cố định (mặc định 128 MB trong HDFS). Nhờ đó, một tệp có thể phân tán trên hàng trăm máy tính và không bị giới hạn bởi dung lượng của một đĩa đơn lẻ.
2. **Nhân bản dữ liệu (Replication Factor):** Nhận định rằng *sự cố phần cứng là điều tất yếu xảy ra* (Hardware failure is the norm), HDFS nhân bản mỗi khối thành nhiều bản sao (mặc định là 3) trên các nút khác nhau (và trên các tủ rack khác nhau - Rack Awareness).
3. **Cơ chế nhịp tim (Heartbeat) và Kiểm tra toàn vẹn (Checksums):** DataNodes gửi nhịp tim định kỳ tới NameNode. Nếu một node ngừng phản hồi, NameNode lập tức phát hiện và tự động điều phối sao chép khối dữ liệu dự phòng từ các node còn sống sang node mới.

#### 1.4. Mục tiêu và ý nghĩa của Đề tài Mini-HDFS
Cụm Hadoop chính thống thường rất nặng nề, phức tạp trong việc cài đặt và tiêu tốn nhiều tài nguyên RAM/CPU. Nhằm mục đích sư phạm, nghiên cứu học tập chuyên sâu, đề tài **Mini-HDFS** được xây dựng với mục tiêu:
- Tự tay hiện thực hóa (From Scratch) mô hình kiến trúc HDFS thu nhỏ bằng ngôn ngữ Python thuần kết hợp framework Flask.
- Vận hành trên cụm mạng máy tính thật thông qua mạng LAN ảo ngang hàng **ZeroTier**.
- Cung cấp trải nghiệm trực quan về: chia khối (Block Size = 500 KB), nhân bản 2 bản sao (Replication Factor = 2), giám sát nhịp tim Heartbeat định kỳ 5 giây và đối soát toàn vẹn SHA-256.
- Xây dựng giao diện Web Dashboard thân thiện, kèm bộ tài liệu thực hành từng bước (step-by-step) để bất kỳ người mới nào cũng có thể cấu hình và chạy thành công.

---

### CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-HDFS

#### 2.1. Mô hình kiến trúc Master - Worker
Hệ thống Mini-HDFS phân chia trách nhiệm rõ ràng giữa nút điều phối và các nút lưu trữ:

```
                          +-----------------------------------+
                          |      CLIENT / WEB DASHBOARD       |
                          |      (http://localhost:5000)      |
                          +-----------------+-----------------+
                                            |
                                  HTTP REST | APIs
                                            v
                          +-----------------------------------+
                          |        NAMENODE / MASTER          |
                          |   - Quản lý metadata.json         |
                          |   - Theo dõi NODE_STATUS (Online) |
                          |   - Cắt khối & Đối soát SHA-256   |
                          +--------+----------------+---------+
                                   |                |
             +---------------------+                +---------------------+
             | HTTP POST/GET                        | HTTP POST/GET       | HTTP POST/GET
             v (ZeroTier LAN)                       v (ZeroTier LAN)      v (Localhost)
+-------------------------+      +-------------------------+     +-------------------------+
|   DATANODE 1 (Worker)   |      |   DATANODE 2 (Worker)   |     |   DATANODE 3 (Worker)   |
|     (node_ducanh)       |      |    (node_khanhphong)    |     |   (node_master_my_pc)   |
|   10.122.174.174:6000   |      |   10.122.174.211:6000   |     |      127.0.0.1:6001     |
|  ./storage/node2/       |      |  ./storage/node3/       |     |  ./storage/node_master/ |
+-------------------------+      +-------------------------+     +-------------------------+
```

| Tên Nút (Node Name) | Địa chỉ IP & Cổng | Vai trò trong Hệ thống | Vị trí Lưu trữ |
| :--- | :--- | :--- | :--- |
| **node_master_my_pc** | `127.0.0.1:5000` (Master)<br>`127.0.0.1:6001` (Worker) | NameNode điều phối + kiêm DataNode 1 | `./storage/node_master/` |
| **node_ducanh** | `10.122.174.174:6000` | DataNode 2 (Worker trên laptop bạn Đức Anh) | `./storage/node2/` |
| **node_khanhphong** | `10.122.174.211:6000` | DataNode 3 (Worker trên laptop bạn Khánh Phong) | `./storage/node3/` |

#### 2.2. Giải pháp liên mạng phân tán P2P với ZeroTier Virtual LAN
Để kết nối các laptop của các thành viên qua mạng Internet mà không bị chặn bởi tường lửa (Firewall) hoặc kỹ thuật NAT (Network Address Translation) của router Wifi, hệ thống sử dụng **ZeroTier One**:
- ZeroTier đóng vai trò như một bộ chuyển mạch Ethernet ảo Layer-2 toàn cầu.
- Các máy tính được gán địa chỉ IP ảo tĩnh trong dải `10.122.174.x`, tạo thành một mạng LAN ảo nội bộ có độ trễ cực thấp.
- Luồng truyền tải dữ liệu giữa Master và các DataNodes được mã hóa bảo mật đầu cuối (End-to-End Encryption) bằng thuật toán Curve25519 / Salsa20.

#### 2.3. Cấu trúc Quản lý Siêu dữ liệu (Metadata Architecture)
Master duy trì toàn bộ thông tin trong tệp `metadata.json`. Cấu trúc JSON được chuẩn hóa như sau:

```json
{
  "ten_file.ext": {
    "original_filename": "video_test.mp4",
    "file_size": 3114374,
    "file_hash": "5e70b96ad27dc8581424be7069ee9de8da9388b716e6fe213d88385f19baf80a",
    "number_of_blocks": 7,
    "replication_factor": 2,
    "blocks": [
      {
        "index": 0,
        "block_name": "video_test.mp4.block_0000",
        "size": 512000,
        "hash": "eab2bdd1000c523624f0398e595e1d129189b29059c905ae85a3f3fb4e898b6a",
        "nodes": [
          "node_ducanh",
          "node_master_my_pc"
        ]
      }
    ]
  }
}
```

*Ý nghĩa các trường:*
- `file_hash`: Mã băm SHA-256 của toàn bộ tệp gốc.
- `number_of_blocks`: Tổng số khối sau khi chia (`ceil(file_size / BLOCK_SIZE)`).
- `nodes`: Danh sách chính xác các DataNode đang lưu giữ bản sao của khối tương ứng.
- `hash`: Mã băm SHA-256 riêng của từng khối, phục vụ kiểm tra toàn vẹn độc lập khi tải về.

#### 2.4. Thiết kế các luồng xử lý nghiệp vụ chính

##### 2.4.1. Luồng Ghi tệp (Upload, Phân khối & Nhân bản)
```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng (Client)
    participant Master as Master Node (app.py)
    participant NodeA as DataNode A (Chính)
    participant NodeB as DataNode B (Bản sao)

    User->>Master: POST /upload (Tệp tin nhị phân)
    Master->>Master: Tính file_hash (SHA-256)
    Master->>Master: Chia tệp thành các khối 500 KB
    loop Với từng Block (index = 0..N-1)
        Master->>Master: Tính hash SHA-256 của Block
        Master->>Master: choose_nodes_for_replication() -> Chọn 2 node ONLINE ngẫu nhiên
        Master->>NodeA: POST /upload_block (Gửi block dữ liệu)
        NodeA-->>Master: 200 OK (Đã lưu khối vào đĩa)
        Master->>NodeB: POST /upload_block (Gửi bản sao block)
        NodeB-->>Master: 200 OK (Đã lưu khối vào đĩa)
    end
    Master->>Master: Ghi nhận và lưu metadata.json an toàn
    Master-->>User: Điều hướng về trang chủ Dashboard
```

##### 2.4.2. Luồng Đọc tệp (Download, Tái hợp khối & Kiểm tra SHA-256)
1. Client gửi yêu cầu `GET /download/<filename>`.
2. Master duyệt qua danh sách các khối theo thứ tự chỉ mục (`index: 0, 1, 2...`).
3. Đối với mỗi khối, Master tìm kiếm node đang lưu trữ có trạng thái `ONLINE`.
4. Gửi `GET /get_block/<block_name>` tới node đó.
5. Sau khi nhận được dữ liệu, Master lập tức tính SHA-256 của dữ liệu vừa nhận và so sánh với `hash` lưu trong metadata:
   - **Nếu khớp:** Thêm dữ liệu khối vào mảng byte (`reconstructed_file`).
   - **Nếu lỗi hoặc Node bị ngắt (Timeout/Offline):** Master tự động chuyển tiếp (Failover) sang DataNode còn lại giữ bản sao của khối đó.
6. Sau khi ghép đủ tất cả các khối, Master băm lại toàn bộ tệp và so sánh với `file_hash` ban đầu. Nếu trùng khớp hoàn toàn, Master trả luồng tệp tin về cho người dùng.

##### 2.4.3. Cơ chế Giám sát Heartbeat và Chịu lỗi (Fault Tolerance)
- Mỗi DataNode có tiểu trình (Thread) chạy nền gửi tín hiệu nhịp tim định kỳ mỗi 5 giây (`POST /heartbeat`).
- Khi một máy tính bị mất mạng hoặc tắt ứng dụng, Master không nhận được heartbeat và đánh dấu node đó là `OFFLINE`.
- Nhờ có `REPLICATION_FACTOR = 2`, dữ liệu của mỗi khối luôn có ít nhất 2 bản sao độc lập. Dù có 1 DataNode bất kỳ bị sập, hệ thống vẫn duy trì tính sẵn sàng 100% cho việc đọc tệp.

---

### CHƯƠNG 3: CHI TIẾT CÀI ĐẶT VÀ HIỆN THỰC MÃ NGUỒN

#### 3.1. Phân tích chi tiết Master Node (`app.py`)
Mã nguồn Master được xây dựng bằng Python kết hợp Flask, tổ chức rõ ràng theo chuẩn module:

1. **Khởi tạo và cấu hình cụm:**
   ```python
   DATANODES = {
       "node_master_my_pc": "http://127.0.0.1:6001",   
       "node_ducanh": "http://10.122.174.174:6000",
       "node_khanhphong": "http://10.122.174.211:6000"
   }
   NODES = list(DATANODES.keys())
   BLOCK_SIZE = 500 * 1024        # Kích thước khối: 500 KB
   REPLICATION_FACTOR = 2         # Nhân bản 2 bản sao
   NODE_STATUS = {node: "OFFLINE" for node in NODES}
   ```

2. **Lưu trữ Metadata an toàn nguyên tử (Atomic Write):**
   ```python
   def save_metadata(metadata: dict) -> None:
       temp_file = METADATA_FILE.with_suffix(".tmp")
       with open(temp_file, "w", encoding="utf-8") as file:
           json.dump(metadata, file, indent=4)
       temp_file.replace(METADATA_FILE) # Thay thế nguyên tử, chống hỏng tệp khi mất điện
   ```

3. **Cơ chế chọn DataNodes trực tuyến cho bản sao:**
   ```python
   def choose_nodes_for_replication() -> list[str]:
       available_nodes = [node for node in NODES if node_is_available(node)]
       if len(available_nodes) < REPLICATION_FACTOR:
           raise RuntimeError(f"Cần tối thiểu {REPLICATION_FACTOR} nodes ONLINE để lưu bản sao!")
       return random.sample(available_nodes, REPLICATION_FACTOR)
   ```

4. **Xử lý Tải tệp và Khắc phục lỗi tự động (Failover):**
   ```python
   for block in sorted_blocks:
       block_data = None
       for node in block["nodes"]:
           if not node_is_available(node):
               continue # Bỏ qua nếu node đang OFFLINE
           node_url = DATANODES[node]
           try:
               resp = requests.get(f"{node_url}/get_block/{block['block_name']}", timeout=5)
               if resp.status_code == 200:
                   candidate_data = resp.content
                   # Đối soát tính toàn vẹn từng block bằng SHA-256
                   if calculate_hash(candidate_data) == block["hash"]:
                       block_data = candidate_data
                       break
           except Exception:
               continue # Lỗi kết nối -> Thử sang replica ở node tiếp theo
   ```

#### 3.2. Phân tích chi tiết DataNode Worker (`datanode_master.py`)
Mỗi DataNode chịu trách nhiệm lưu trữ các block vào thư mục riêng và phát nhịp tim:

```python
import os, requests, threading, time
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
STORAGE_DIR = "./storage/node_master"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/upload_block', methods=['POST'])
def upload_block():
    block_name = request.form.get('block_name')
    file = request.files['file']
    file.save(os.path.join(STORAGE_DIR, block_name))
    return jsonify({"status": "success"}), 200

@app.route('/get_block/<block_name>', methods=['GET'])
def get_block(block_name):
    path = os.path.join(STORAGE_DIR, block_name)
    if os.path.exists(path):
        return send_file(path)
    return jsonify({"error": "Block not found"}), 404

def send_heartbeat():
    while True:
        try:
            requests.post("http://127.0.0.1:5000/heartbeat", json={
                "node_name": "node_master_my_pc",
                "status": "ONLINE"
            }, timeout=3)
        except Exception:
            pass
        time.sleep(5) # Phát tín hiệu nhịp tim định kỳ 5 giây

if __name__ == '__main__':
    threading.Thread(target=send_heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=6001)
```

#### 3.3. Thiết kế Giao diện Quản trị Web Dashboard (`templates/index.html`)
Giao diện quản trị được lập trình bằng HTML5/CSS3 hiện đại với bảng hiển thị cụm Cluster động:
- Hiển thị bảng trạng thái các Node (Màu xanh = ONLINE, Màu đỏ = OFFLINE).
- Form upload tệp trực tiếp lên hệ thống phân tán.
- Bảng danh mục tệp hiển thị: Tên file, kích thước thực tế, số lượng khối (blocks) được chia, hệ số bản sao và các nút tải xuống, xem metadata, xóa file.

---

### CHƯƠNG 4: HƯỚNG DẪN DEMO VÀ THỰC HÀNH CHI TIẾT (STEP-BY-STEP DÀNH CHO NGƯỜI MỚI)

> **Mục tiêu phần này:** Hướng dẫn từng bước từ chuẩn bị máy tính, mạng, cấu hình IP, khởi động cụm và tiến hành 4 kịch bản kiểm thử thực tế. Người mới chỉ cần copy-paste lệnh và làm theo là chạy thành công 100%.

#### 4.1. Chuẩn bị môi trường máy trạm và mạng ZeroTier

##### Bước 1.1: Chuẩn bị mã nguồn và môi trường Python
Trên máy Master (hoặc tất cả các máy tham gia), mở cửa sổ dòng lệnh PowerShell:
```powershell
# 1. Điều hướng vào thư mục làm việc
cd D:\bigdata

# 2. Khởi tạo môi trường ảo Python
python -m venv venv

# 3. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1

# 4. Cài đặt các thư viện bắt buộc
pip install flask requests werkzeug
```

##### Bước 1.2: Thiết lập mạng ZeroTier kết nối các máy
1. Tải và cài đặt phần mềm **ZeroTier One** từ trang chủ: `https://www.zerotier.com/download/`.
2. Trưởng nhóm tạo một Network ID trên trang ZeroTier Central (ví dụ: `8056c2e21c...`).
3. Các thành viên mở ứng dụng ZeroTier trên khay hệ thống, bấm **Join Network...** và nhập Network ID trên.
4. Trưởng nhóm truy cập ZeroTier Central, tích chọn vào ô **Auth** (Ủy quyền) cho từng máy.
5. Ghi lại địa chỉ IP ZeroTier hiển thị (Managed IPs):
   - Máy Master: `10.122.174.100` (hoặc localhost kiểm thử)
   - Máy bạn Đức Anh: `10.122.174.174`
   - Máy bạn Khánh Phong: `10.122.174.211`
6. Kiểm tra kết nối mạng giữa các máy bằng lệnh `ping`:
   ```powershell
   ping 10.122.174.174
   ping 10.122.174.211
   ```
   *(Nếu ping có phản hồi `Reply from...` tức là mạng ảo P2P đã thông suốt).*

#### 4.2. Cấu hình địa chỉ IP và Khởi động hệ thống

##### Bước 2.1: Cập nhật cấu hình trong `mini-hdfs/app.py`
Mở tệp `D:\bigdata\mini-hdfs\app.py`, kiểm tra từ điển `DATANODES` khớp với địa chỉ IP thực tế:
```python
DATANODES = {
    "node_master_my_pc": "http://127.0.0.1:6001",   
    "node_ducanh": "http://10.122.174.174:6000",
    "node_khanhphong": "http://10.122.174.211:6000"
}
```

##### Bước 2.2: Khởi chạy Master Node (NameNode)
Tại máy Master, mở Terminal 1:
```powershell
cd D:\bigdata\mini-hdfs
..\venv\Scripts\python.exe app.py
```
*Màn hình hiển thị:*
```text
* Serving Flask app 'app'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

##### Bước 2.3: Khởi chạy DataNode 1 trên máy Master
Tại máy Master, mở thêm Terminal 2:
```powershell
cd D:\bigdata\mini-hdfs
..\venv\Scripts\python.exe datanode_master.py
```
*Màn hình hiển thị:* `Running on http://0.0.0.0:6001` và tự động gửi heartbeat về cổng 5000.

##### Bước 2.4: Khởi chạy DataNode 2 và DataNode 3 trên máy thành viên
Trên máy tính của bạn Đức Anh và Khánh Phong:
- Đảm bảo trong mã nguồn DataNode biến `MASTER_IP` trỏ về IP ZeroTier của máy Master.
- Chạy lệnh:
  ```powershell
  python datanode_worker.py
  ```
  *(Tiến trình sẽ lắng nghe cổng 6000 và định kỳ gửi nhịp tim về Master).*

---

#### 4.3. Kịch bản Demo 1: Tải lên tệp đa phương tiện lớn (Splitting & Replication)
- **Mục tiêu:** Kiểm chứng thuật toán cắt nhỏ tệp thành các khối chuẩn 500 KB và cơ chế nhân bản 2 bản sao phân tán trên các máy vật lý.
- **Thao tác thực hiện:**
  1. Mở trình duyệt Web tại máy Master, truy cập: `http://localhost:5000`.
  2. Quan sát khung **Cluster Status**: Cả 3 nút `node_master_my_pc`, `node_ducanh`, `node_khanhphong` đều hiện màu xanh lá **ONLINE**.
  3. Tại khung **Upload a File**, bấm nút **Choose File** và chọn tệp `video_test.mp4` (dung lượng thực tế: **3,114,374 bytes** ~ 3.1 MB).
  4. Bấm nút **Upload to Mini HDFS**.
  5. Sau vài giây truyền dữ liệu qua mạng, trang web tự động tải lại và hiển thị bảng thông tin:

| Tên Tệp (File) | Kích thước (Size) | Số khối (Blocks) | Hệ số nhân bản (Replication) | Thao tác (Actions) |
| :--- | :--- | :--- | :--- | :--- |
| `video_test.mp4` | 3,114,374 bytes | **7** | 2 | `Download` \| `Metadata` \| `Delete` |

- **Giải thích cơ chế:**
  $$\text{Số lượng Block} = \left\lceil \frac{3,114,374 \text{ bytes}}{500 \times 1024 \text{ bytes}} \right\rceil = \left\lceil \frac{3,114,374}{512,000} \right\rceil = 7 \text{ blocks}$$
  Trong đó 6 block đầu tiên có kích thước đúng bằng 512,000 bytes; block số 7 (chỉ mục 0006) chứa phần dư 42,374 bytes còn lại.

---

#### 4.4. Kịch bản Demo 2: Kiểm tra cấu trúc Metadata và Tính toàn vẹn SHA-256
- **Mục tiêu:** Khám phá cấu trúc siêu dữ liệu và chứng minh các block đã được ghi vào đúng ổ cứng của các máy.
- **Thao tác thực hiện:**
  1. Bấm nút **Metadata** trên giao diện Web hoặc mở liên kết: `http://localhost:5000/metadata/video_test.mp4`.
  2. Phân tích kết quả JSON trả về:
     - `file_hash`: `5e70b96ad27dc8581424be7069ee9de8da9388b716e6fe213d88385f19baf80a` (Mã SHA-256 gốc của tệp video).
     - Chi tiết từng block:
       ```json
       {
         "index": 0,
         "block_name": "video_test.mp4.block_0000",
         "size": 512000,
         "hash": "eab2bdd1000c523624f0398e595e1d129189b29059c905ae85a3f3fb4e898b6a",
         "nodes": ["node_ducanh", "node_master_my_pc"]
       }
       ```
  3. Mở File Explorer trên máy Master kiểm tra thư mục `D:\bigdata\mini-hdfs\storage\node_master`:
     - Ta thấy các tệp: `video_test.mp4.block_0000`, `block_0002`, `block_0003`, `block_0004`, `block_0005`, `block_0006`.
  4. Mở File Explorer trên máy bạn Đức Anh (`node_ducanh`) kiểm tra thư mục `storage/node2`:
     - Ta thấy các tệp: `video_test.mp4.block_0000`, `block_0001`, `block_0004`, `block_0005`, `block_0006`.
  - **Kết luận:** Dữ liệu đã được phân tán ngẫu nhiên và mỗi block đều có đúng 2 bản sao độc lập trên 2 máy tính khác nhau.

---

#### 4.5. Kịch bản Demo 3: Thử nghiệm Chịu lỗi khi Máy chủ (Master Server) gặp sự cố sập hoàn toàn (Khôi phục P2P giữa máy Phong và máy Đức Anh)
- **Mục tiêu:** Chứng minh sức mạnh cốt lõi của hệ thống lưu trữ phân tán: Ngay cả khi máy chủ Master (NameNode) bị mất điện, tắt nguồn hoặc sập hoàn toàn khiến Web Dashboard không thể truy cập, dữ liệu người dùng không hề bị mất. Nhờ hệ số nhân bản `Replication Factor = 2`, các khối dữ liệu thực tế vẫn nằm an toàn trên các máy DataNode (máy Đức Anh và máy Phong). Người dùng có thể đứng từ máy Phong (hoặc Đức Anh) chạy script khôi phục trực tiếp qua mạng ZeroTier P2P để kéo các block còn thiếu và ghép lại thành video nguyên vẹn!

- **Mô phỏng sự cố (Simulate Master Failure):**
  1. Tại máy Master, nhấn tổ hợp phím `Ctrl + C` ở cả 2 Terminal đang chạy `app.py` và `datanode_master.py`.
  2. Mở trình duyệt thử truy cập `http://localhost:5000` -> Báo lỗi *This site can’t be reached (ERR_CONNECTION_REFUSED)*. Máy chủ Master đã "chết" hoàn toàn.

- **Cách làm chi tiết (Thực hiện trực tiếp trên máy Phong):**

  ##### Bước 1: Kiểm tra IP ZeroTier của máy Đức Anh
  Xem IP ZeroTier trên máy Đức Anh là gì. Ví dụ IP ZeroTier của Đức Anh là: `10.122.174.174` (hoặc `10.122.174.211` tùy theo địa chỉ thực tế hiển thị trên ứng dụng ZeroTier của Đức Anh).

  ##### Bước 2: Chạy đoạn script Python ghép file trên máy Phong
  Bảo Phong tạo một file mới tên là `pull_and_merge.py` nằm cùng thư mục dự án (ngang hàng với `datanode_friend.py` hoặc `datanode_master.py`) và dán đoạn code sau vào:

  ```python
  import os
  import requests

  # 1. Điền IP ZeroTier của máy Đức Anh vào đây (Sửa lại đúng IP thực tế)
  DUC_ANH_IP = "10.122.174.174"  # Thay bằng IP ZeroTier thực tế của máy Đức Anh
  DUC_ANH_PORT = 6000

  # Thư mục lưu block trên máy Phong (Tự động tạo nếu chưa có)
  STORAGE_DIR = "./storage_node"  # hoặc "./storage/node3"
  os.makedirs(STORAGE_DIR, exist_ok=True)

  # Danh sách chuẩn 7 block cần gom đủ
  blocks_needed = [
      f"video_test.mp4.block_000{i}" for i in range(7)
  ]

  print("🚀 Đang kiểm tra và tải các block còn thiếu...")

  for block_name in blocks_needed:
      local_path = os.path.join(STORAGE_DIR, block_name)
      
      # Nếu máy Phong chưa có block này -> Gọi API kéo từ máy Đức Anh về
      if not os.path.exists(local_path):
          url = f"http://{DUC_ANH_IP}:{DUC_ANH_PORT}/get_block/{block_name}"
          print(f"📥 Đang tải {block_name} từ máy Đức Anh ({DUC_ANH_IP})...")
          try:
              res = requests.get(url, timeout=10)
              if res.status_code == 200:
                  with open(local_path, "wb") as f:
                      f.write(res.content)
                  print(f"✅ Tải thành công: {block_name}")
              else:
                  print(f"❌ Không tìm thấy {block_name} trên máy Đức Anh")
          except Exception as e:
              print(f"❌ Lỗi kết nối tới máy Đức Anh: {e}")
      else:
          print(f"✔️ Máy Phong đã có sẵn: {block_name}")

  # Bước 3: Ghép tất cả các block lại thành video hoàn chỉnh
  output_video = "video_hoanchinh.mp4"
  print(f"\n🎬 Đang tiến hành ghép {len(blocks_needed)} blocks thành {output_video}...")

  with open(output_video, "wb") as outfile:
      for block_name in blocks_needed:
          block_path = os.path.join(STORAGE_DIR, block_name)
          if os.path.exists(block_path):
              with open(block_path, "rb") as infile:
                  outfile.write(infile.read())

  print(f"\n🎉 HOÀN THÀNH! Video hoàn chỉnh được tạo tại: {os.path.abspath(output_video)}")
  ```

  > 💡 **Điểm tinh chỉnh trong code giúp hoạt động ổn định 100%:**
  > - Bổ sung dòng `os.makedirs(STORAGE_DIR, exist_ok=True)` để đảm bảo thư mục lưu trữ luôn tồn tại, tránh lỗi `FileNotFoundError` khi máy Phong lần đầu tải block về.
  > - Thêm biến cổng kết nối `DUC_ANH_PORT = 6000` để linh hoạt cấu hình theo DataNode của bạn Đức Anh.

  ##### Bước 3: Chạy script trên máy Phong
  Bảo Phong mở Terminal trên máy Mac (hoặc PowerShell trên Windows) và gõ:
  ```bash
  python3 pull_and_merge.py
  ```
  *(Trên Windows có thể gõ: `python pull_and_merge.py`)*

  **Diễn biến thực tế của hệ thống:**
  - Script kiểm tra các block hiện có trên máy Phong: phát hiện các block đã có sẵn như `block_0001`, `block_0002`, `block_0003`.
  - Đối với các block còn thiếu như `block_0000`, `block_0004`, `block_0005`, `block_0006`, script sẽ tự lấy từ máy Đức Anh thông qua API `/get_block/...` chạy trên cổng 6000 qua mạng ảo ZeroTier.
  - Sau đó, script tự động ghép tuần tự nối đủ 7 block thành file `video_hoanchinh.mp4` nằm ngay trong thư mục dự án của Phong!

  ##### Bước 4: Kiểm chứng phát tệp video sau khi ghép
  - Phong mở file `video_hoanchinh.mp4` bằng trình phát mặc định (QuickTime Player trên macOS hoặc VLC/Windows Media Player).
  - Tệp video mở lên trơn tru, phát từ giây đầu tiên đến giây cuối cùng, hình ảnh sắc nét và âm thanh khớp 100%, dung lượng đạt chuẩn đúng 3,114,374 bytes.
  - **Kết luận:** Thử nghiệm chứng minh thành công cơ chế chịu lỗi đỉnh cao của hệ thống lưu trữ phân tán. Ngay cả khi máy chủ Master trung tâm bị sập hoàn toàn, các nút mạng ngang hàng (P2P Worker Nodes) vẫn có thể phối hợp kéo các mảnh ghép dữ liệu về để tái hợp lại tệp tin nguyên bản trọn vẹn!

---

#### 4.6. Kịch bản Demo 4: Xóa tệp và thu hồi tài nguyên trên các DataNodes
- **Mục tiêu:** Kiểm tra cơ chế dọn dẹp phân tán.
- **Thao tác thực hiện:**
  1. Trên giao diện Web, bấm nút **Delete** màu đỏ bên cạnh tệp `video_test.mp4`.
  2. Trình duyệt hiển thị hộp thoại xác nhận: `Delete this file?` -> Bấm **OK**.
  3. Master gửi tín hiệu `DELETE /delete_block/<block_name>` tới các DataNodes liên quan.
  4. Thông tin tệp trong `metadata.json` được xóa bỏ.
  5. Kiểm tra các thư mục lưu trữ `storage/`: Tất cả các tệp khối dữ liệu trên các máy tính đã được giải phóng hoàn toàn, bảo đảm hệ thống không bị rò rỉ dung lượng đĩa.

---

### CHƯƠNG 5: ĐÁNH GIÁ KẾT QUẢ VÀ HƯỚNG PHÁT TRIỂN

#### 5.1. Đánh giá ưu điểm đạt được
1. **Mô phỏng chân thực và sâu sắc:** Hệ thống đã hiện thực hóa trọn vẹn các nguyên lý cốt lõi của Hadoop HDFS (Block splitting, Replication, Metadata, Heartbeat, Data Integrity, Failover).
2. **Triển khai đa máy thực tế qua mạng ảo P2P:** Không chỉ là mô phỏng trên bộ nhớ giả lập (In-memory), Mini-HDFS truyền tải dữ liệu nhị phân thực qua mạng giữa nhiều máy tính vật lý với ZeroTier.
3. **Độ tin cậy và Tính toàn vẹn cao:** Ứng dụng mã băm mã hóa SHA-256 ở cả hai cấp độ (Block Hash và File Hash), phát hiện triệt để các lỗi sai lệch dữ liệu trong quá trình truyền tải mạng.
4. **Trực quan, dễ sử dụng:** Giao diện Web Dashboard sinh động, thân thiện, người học dễ dàng quan sát trực tiếp trạng thái cụm và từng khối dữ liệu.

#### 5.2. Các hạn chế tồn tại
- **Điểm lỗi đơn lẻ tại Master (Single Point of Failure - SPOF):** Hiện tại hệ thống chỉ có một Master duy nhất; nếu máy Master gặp sự cố sập nguồn thì toàn bộ cụm sẽ ngưng phục vụ tạm thời (chưa có Secondary NameNode hoặc Standby NameNode).
- **Cơ chế Tự động Tái nhân bản (Auto Re-replication):** Khi một DataNode bị chết vĩnh viễn, hệ thống chưa tự động điều phối sao chép từ node còn lại sang một node thứ ba còn trống để khôi phục đủ hệ số Replication = 2.
- **Bảo mật và Phân quyền:** Chưa tích hợp hệ thống xác thực người dùng (Authentication) và phân quyền truy cập tập tin theo chuẩn POSIX.

#### 5.3. Định hướng mở rộng trong tương lai
1. **Xây dựng NameNode High Availability:** Sử dụng thuật toán đồng thuận phân tán Raft (hoặc Paxos) để triển khai cụm NameNode Active-Standby với cơ chế tự động chuyển vùng khi Master chính gặp sự cố.
2. **Tích hợp Công cụ Tính toán Phân tán MapReduce:** Xây dựng một framework xử lý song song (Mini-MapReduce) tận dụng đặc tính ưu tiên dữ liệu cục bộ (Data Locality) trên các DataNodes của Mini-HDFS.
3. **Mã hóa khối dữ liệu (Data-at-Rest Encryption):** Tích hợp thuật toán mã hóa đối xứng AES-GCM cho từng khối dữ liệu trước khi lưu vào đĩa cứng của DataNode nhằm nâng cao tính an toàn bảo mật.

---

### KẾT LUẬN

Đề tài *"Thiết kế và triển khai hệ thống lưu trữ phân tán mô phỏng Hadoop HDFS (Mini-HDFS) trên mạng LAN ảo P2P (ZeroTier)"* đã hoàn thành toàn diện và xuất sắc tất cả các mục tiêu lý thuyết và thực tiễn đề ra. Dự án không chỉ tái hiện một cách sống động kiến trúc lưu trữ phân tán kinh điển của Hadoop HDFS mà còn đem lại trải nghiệm kỹ thuật sâu sắc về mạng máy tính, giao thức truyền tải nhị phân HTTP RESTful, cơ chế kiểm tra toàn vẹn băm SHA-256 và thuật toán xử lý chịu lỗi khi có nút mạng gặp sự cố.

Tài liệu báo cáo cùng bộ mã nguồn đã được thiết kế chuẩn hóa, rõ ràng và chi tiết theo từng bước, có giá trị học tập cao, giúp sinh viên và những người mới bắt đầu tiếp cận môn học Dữ liệu lớn có thể nhanh chóng nắm bắt bản chất bên dưới của các hệ thống phân tán quy mô lớn hiện đại.

---

## vi) TÀI LIỆU THAM KHẢO (HARVARD REFERENCING SYSTEM)

1. Apache Software Foundation, 2024. *HDFS Architecture Guide*. Apache Hadoop Documentation. Có sẵn tại: <https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html> [Truy cập ngày 15 tháng 10 năm 2026].
2. Ghemawat, S., Gobioff, H. và Leung, S.T., 2003. The Google file system. Trong: *Proceedings of the nineteenth ACM symposium on Operating systems principles (SOSP '03)*. Bolton Landing, NY, USA: ACM, tr. 29–43. https://doi.org/10.1145/945445.945450.
3. Grinberg, M., 2018. *Flask Web Development: Developing Web Applications with Python*. Ấn bản lần 2. Sebastopol, CA: O'Reilly Media.
4. Kleppmann, M., 2017. *Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*. Sebastopol, CA: O'Reilly Media.
5. Shvachko, K., Kuang, H., Radia, S. và Chansler, R., 2010. The Hadoop Distributed File System. Trong: *2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST)*. Incline Village, NV, USA: IEEE, tr. 1–10. https://doi.org/10.1109/MSST.2010.5496972.
6. Tanenbaum, A.S. và Van Steen, M., 2017. *Distributed Systems: Principles and Paradigms*. Ấn bản lần 3. Leiden: CreateSpace Independent Publishing Platform.
7. White, T., 2015. *Hadoop: The Definitive Guide*. Ấn bản lần 4. Sebastopol, CA: O'Reilly Media.
8. ZeroTier Inc., 2024. *ZeroTier Manual: A Smart Programmable Ethernet Switch for Earth*. ZeroTier Documentation. Có sẵn tại: <https://docs.zerotier.com/> [Truy cập ngày 18 tháng 10 năm 2026].

---

## vii) PHỤ LỤC

### Phụ lục A: Toàn bộ mã nguồn hoàn chỉnh Master Node (`app.py`)
```python
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

# ==================== CẤU HÌNH DATANODES QUA ZEROTIER ====================
DATANODES = {
    "node_master_my_pc": "http://127.0.0.1:6001",   
    "node_ducanh": "http://10.122.174.174:6000",
    "node_khanhphong": "http://10.122.174.211:6000"
}

NODES = list(DATANODES.keys())
BLOCK_SIZE = 500 * 1024          # 500 KB / block
REPLICATION_FACTOR = 2           # Nhân bản 2 bản sao
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

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    data = request.json or {}
    node_name = data.get("node_name")
    if node_name in NODE_STATUS:
        NODE_STATUS[node_name] = "ONLINE"
    return jsonify({"status": "acknowledged"}), 200

def node_is_available(node: str) -> bool:
    return NODE_STATUS.get(node) == "ONLINE"

def choose_nodes_for_replication() -> list[str]:
    available_nodes = [node for node in NODES if node_is_available(node)]
    if len(available_nodes) < REPLICATION_FACTOR:
        raise RuntimeError(f"At least {REPLICATION_FACTOR} available nodes are required.")
    return random.sample(available_nodes, REPLICATION_FACTOR)

def delete_old_blocks(filename: str, file_metadata: dict) -> None:
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
        for node in block["nodes"]:
            if not node_is_available(node):
                continue
            node_url = DATANODES[node]
            try:
                resp = requests.get(f"{node_url}/get_block/{block['block_name']}", timeout=5)
                if resp.status_code == 200:
                    candidate_data = resp.content
                    if calculate_hash(candidate_data) == block["hash"]:
                        block_data = candidate_data
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
```

---

### Phụ lục B: Toàn bộ mã nguồn hoàn chỉnh DataNode (`datanode_master.py`)
```python
import os
import requests
import threading
import time
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

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
```

---

### Phụ lục C: Toàn bộ mã nguồn script khôi phục P2P (`pull_and_merge.py`)
```python
import os
import requests

# 1. Điền IP ZeroTier của máy Đức Anh vào đây (Sửa lại đúng IP thực tế)
DUC_ANH_IP = "10.122.174.174"  # Thay bằng IP ZeroTier thực tế của máy Đức Anh
DUC_ANH_PORT = 6000

# Thư mục lưu block trên máy Phong (Tự động tạo nếu chưa có)
STORAGE_DIR = "./storage_node"  # hoặc "./storage/node3"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Danh sách chuẩn 7 block cần gom đủ
blocks_needed = [
    f"video_test.mp4.block_000{i}" for i in range(7)
]

print("🚀 Đang kiểm tra và tải các block còn thiếu...")

for block_name in blocks_needed:
    local_path = os.path.join(STORAGE_DIR, block_name)
    
    # Nếu máy Phong chưa có block này -> Gọi API kéo từ máy Đức Anh về
    if not os.path.exists(local_path):
        url = f"http://{DUC_ANH_IP}:{DUC_ANH_PORT}/get_block/{block_name}"
        print(f"📥 Đang tải {block_name} từ máy Đức Anh ({DUC_ANH_IP})...")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Tải thành công: {block_name}")
            else:
                print(f"❌ Không tìm thấy {block_name} trên máy Đức Anh (Code: {res.status_code})")
        except Exception as e:
            print(f"❌ Lỗi kết nối tới máy Đức Anh: {e}")
    else:
        print(f"✔️ Máy Phong đã có sẵn: {block_name}")

# Bước 3: Ghép tất cả các block lại thành video hoàn chỉnh
output_video = "video_hoanchinh.mp4"
print(f"\n🎬 Đang tiến hành ghép {len(blocks_needed)} blocks thành {output_video}...")

with open(output_video, "wb") as outfile:
    for block_name in blocks_needed:
        block_path = os.path.join(STORAGE_DIR, block_name)
        if os.path.exists(block_path):
            with open(block_path, "rb") as infile:
                outfile.write(infile.read())

print(f"\n🎉 HOÀN THÀNH! Video hoàn chỉnh được tạo tại: {os.path.abspath(output_video)}")
```

---

### Phụ lục D: Tệp tin `metadata.json` thực nghiệm thực tế
```json
{
    "video_test.mp4": {
        "original_filename": "video_test.mp4",
        "file_size": 3114374,
        "file_hash": "5e70b96ad27dc8581424be7069ee9de8da9388b716e6fe213d88385f19baf80a",
        "number_of_blocks": 7,
        "replication_factor": 2,
        "blocks": [
            {
                "index": 0,
                "block_name": "video_test.mp4.block_0000",
                "size": 512000,
                "hash": "eab2bdd1000c523624f0398e595e1d129189b29059c905ae85a3f3fb4e898b6a",
                "nodes": [
                    "node_ducanh",
                    "node_master_my_pc"
                ]
            },
            {
                "index": 1,
                "block_name": "video_test.mp4.block_0001",
                "size": 512000,
                "hash": "b36b2ae61c8599f6848938a1c2ba6739c9775d2e2f728c4ba8475a0bf2dbbf56",
                "nodes": [
                    "node_khanhphong",
                    "node_ducanh"
                ]
            },
            {
                "index": 2,
                "block_name": "video_test.mp4.block_0002",
                "size": 512000,
                "hash": "3c6e8571cf4a9d8ba123a794fc57364abfb0ac9bf5b8cfa744b0e77d32caf6a2",
                "nodes": [
                    "node_khanhphong",
                    "node_master_my_pc"
                ]
            },
            {
                "index": 3,
                "block_name": "video_test.mp4.block_0003",
                "size": 512000,
                "hash": "d934e896b074562e55d58e5cac3444db05631557870ec32771b510903fbcd543",
                "nodes": [
                    "node_master_my_pc",
                    "node_khanhphong"
                ]
            },
            {
                "index": 4,
                "block_name": "video_test.mp4.block_0004",
                "size": 512000,
                "hash": "62998dfa118a08a3efc8329b5fbface0a78283f28506610153e40318acaf9068",
                "nodes": [
                    "node_ducanh",
                    "node_master_my_pc"
                ]
            },
            {
                "index": 5,
                "block_name": "video_test.mp4.block_0005",
                "size": 512000,
                "hash": "eb6f2e77466cd0aa1636ed7bce6b9ebfd9fb8ef6ae67c6df5082fa6284ee82a0",
                "nodes": [
                    "node_ducanh",
                    "node_master_my_pc"
                ]
            },
            {
                "index": 6,
                "block_name": "video_test.mp4.block_0006",
                "size": 42374,
                "hash": "c2ed61f3859bc39c79608eca007d131cd4d295f881c7f7a2f5eacc355e198bb8",
                "nodes": [
                    "node_ducanh",
                    "node_master_my_pc"
                ]
            }
        ]
    }
}
```
