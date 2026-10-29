import os
import requests

# ==============================================================================
# SCRIPT KÉO BLOCK VÀ GHÉP TỆP P2P TRÊN MÁY WORKER KHI MASTER GẶP SỰ CỐ
# ==============================================================================

# 1. Điền IP ZeroTier của máy bạn Đức Anh vào đây (Kiểm tra IP thực tế qua ZeroTier)
# Ví dụ: nếu IP Đức Anh là 10.122.174.174 hoặc 10.122.174.211 thì điền vào đây
DUC_ANH_IP = "10.122.174.174" 
DUC_ANH_PORT = 6000

# Thư mục lưu block trên máy Phong (Tự động tạo nếu chưa tồn tại)
STORAGE_DIR = "./storage/node3"  # hoặc "./storage_node" tùy theo đường dẫn trên máy Phong
os.makedirs(STORAGE_DIR, exist_ok=True)

# Danh sách 7 block của tệp video_test.mp4 cần gom đủ
blocks_needed = [
    f"video_test.mp4.block_000{i}" for i in range(7)
]

print("=" * 60)
print("🚀 HỆ THỐNG PHỤC HỒI P2P: KIỂM TRA VÀ TẢI CÁC BLOCK CÒN THIẾU")
print(f"📡 Kết nối tới DataNode Đức Anh tại: http://{DUC_ANH_IP}:{DUC_ANH_PORT}")
print("=" * 60)

missing_count = 0
success_download = 0

for block_name in blocks_needed:
    local_path = os.path.join(STORAGE_DIR, block_name)
    
    # Nếu máy Phong chưa có block này -> Gọi API kéo trực tiếp từ máy Đức Anh về
    if not os.path.exists(local_path):
        missing_count += 1
        url = f"http://{DUC_ANH_IP}:{DUC_ANH_PORT}/get_block/{block_name}"
        print(f"📥 Đang tải {block_name} từ máy Đức Anh ({DUC_ANH_IP})...")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(res.content)
                print(f"  ✅ Tải thành công: {block_name} ({len(res.content)} bytes)")
                success_download += 1
            else:
                print(f"  ❌ Không tìm thấy {block_name} trên máy Đức Anh (Mã lỗi: {res.status_code})")
        except Exception as e:
            print(f"  ❌ Lỗi kết nối tới máy Đức Anh: {e}")
    else:
        print(f"✔️ Máy Phong đã có sẵn: {block_name}")

print("-" * 60)
print(f"📊 Thống kê: Thiếu {missing_count} blocks | Đã kéo về thành công {success_download} blocks")

# Bước 3: Ghép tất cả các block lại thành video hoàn chỉnh
output_video = "video_hoanchinh.mp4"
print(f"\n🎬 Đang tiến hành ghép {len(blocks_needed)} blocks thành {output_video}...")

all_blocks_present = True
for block_name in blocks_needed:
    block_path = os.path.join(STORAGE_DIR, block_name)
    if not os.path.exists(block_path):
        print(f"⚠️ CẢNH BÁO: Thiếu khối dữ liệu {block_name}, video ghép ra có thể bị gián đoạn!")
        all_blocks_present = False

with open(output_video, "wb") as outfile:
    for block_name in blocks_needed:
        block_path = os.path.join(STORAGE_DIR, block_name)
        if os.path.exists(block_path):
            with open(block_path, "rb") as infile:
                outfile.write(infile.read())

if all_blocks_present:
    print(f"\n🎉 HOÀN THÀNH XUẤT SẮC! Đã ghép đủ 100% {len(blocks_needed)} blocks.")
else:
    print(f"\n⚠️ Đã ghép các block hiện có.")

print(f"📁 Video hoàn chỉnh được tạo tại: {os.path.abspath(output_video)}")
print(f"📊 Dung lượng file: {os.path.getsize(output_video):,} bytes")
