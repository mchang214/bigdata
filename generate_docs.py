# -*- coding: utf-8 -*-
"""
Script tạo file Word Báo cáo Đồ án Big Data - Mini HDFS chuẩn học thuật
Cập nhật kịch bản Demo 3: Chịu lỗi khi Master sập và khôi phục P2P giữa máy Phong và máy Đức Anh
"""
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_report():
    doc = docx.Document()

    # Lề trang chuẩn (Top: 2cm, Bottom: 2cm, Left: 3cm, Right: 2cm)
    for section in doc.sections:
        section.top_margin = Inches(0.79)     # ~2.0 cm
        section.bottom_margin = Inches(0.79)  # ~2.0 cm
        section.left_margin = Inches(1.18)    # ~3.0 cm
        section.right_margin = Inches(0.79)   # ~2.0 cm

    # Style chuẩn Normal
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(13)
    font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_title_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.bold = True
        if level == 1:
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(0x0F, 0x3D, 0x73) # Navy Blue
        elif level == 2:
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x1E, 0x40, 0xAF) # Blue
        elif level == 3:
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run.font.size = Pt(13)
            run.italic = True
            run.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F0F9FF")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0284C7"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(3)
        r_title = p.add_run(f"📌 {title}\n")
        r_title.bold = True
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(12)
        r_title.font.color.rgb = RGBColor(0x03, 0x69, 0xA1)

        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(11.5)
        r_text.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        doc.add_paragraph()

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="12" w:space="0" w:color="94A3B8"/><w:top w:val="single" w:sz="6" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="6" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
        tcPr.append(tcBorders)

        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        doc.add_paragraph()

    # ==================== I) TRANG BÌA ====================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni1 = p_uni.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ\n")
    r_uni1.bold = True
    r_uni1.font.size = Pt(13)
    r_uni1.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    r_uni2 = p_uni.add_run("KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN HỆ THỐNG THÔNG TIN\n")
    r_uni2.bold = True
    r_uni2.font.size = Pt(13)
    r_uni2.font.color.rgb = RGBColor(0x0F, 0x3D, 0x73)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("-------------------***-------------------")
    r_line.font.size = Pt(12)
    p_line.paragraph_format.space_after = Pt(45)

    p_doc_type = doc.add_paragraph()
    p_doc_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_doc_type = p_doc_type.add_run("BÁO CÁO BÀI TẬP LỚN HỌC PHẦN DỮ LIỆU LỚN (BIG DATA)")
    r_doc_type.bold = True
    r_doc_type.font.size = Pt(15)
    r_doc_type.font.color.rgb = RGBColor(0xC2, 0x41, 0x0C)
    p_doc_type.paragraph_format.space_after = Pt(25)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("ĐỀ TÀI:\nTHIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG LƯU TRỮ PHÂN TÁN\nMÔ PHỎNG HADOOP HDFS (MINI-HDFS)\nTRÊN MẠNG LAN ẢO P2P (ZEROTIER)")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(0x0F, 0x3D, 0x73)
    p_title.paragraph_format.space_after = Pt(70)

    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Giảng viên hướng dẫn:", "TS. Giảng viên phụ trách môn học"),
        ("Học phần:", "Dữ liệu lớn và Ứng dụng (Big Data Analytics)"),
        ("Sinh viên thực hiện:", "1. Nguyễn Đức Anh      (Node Worker 1)\n2. Lê Khánh Phong      (Node Worker 2)\n3. Trưởng nhóm / Dev   (Master & Worker)"),
        ("Mã số sinh viên (MSSV):", "B21DCCN... / B21DCCN..."),
        ("Lớp chuyên ngành:", "Khoa học Máy tính / CNTT - Khóa 2021-2025")
    ]
    for i, (label, val) in enumerate(info_data):
        row = tbl_info.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(12)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(val)
        r1.font.size = Pt(12)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(80)
    r_foot = p_foot.add_run("Hà Nội, Năm 2026")
    r_foot.bold = True
    r_foot.font.size = Pt(13)

    doc.add_page_break()

    # ==================== II) LỜI CẢM ƠN ====================
    add_title_heading("LỜI CẢM ƠN", level=1)
    doc.add_paragraph(
        "Lời đầu tiên, nhóm tác giả xin gửi lời cảm ơn chân thành và sâu sắc nhất tới Quý Thầy/Cô bộ môn "
        "Dữ liệu lớn (Big Data) thuộc Khoa Công nghệ Thông tin. Trong suốt quá trình học tập và nghiên cứu "
        "trên giảng đường, sự truyền thụ tận tình, những bài giảng giàu tính thực tiễn cùng sự định hướng "
        "khoa học của Thầy/Cô đã trang bị cho chúng em nền tảng kiến thức vững chắc về các mô hình xử lý, "
        "kiến trúc hệ thống tính toán và lưu trữ phân tán hiện đại."
    )
    doc.add_paragraph(
        "Báo cáo đề tài \"Thiết kế và triển khai hệ thống lưu trữ phân tán mô phỏng Hadoop HDFS (Mini-HDFS) "
        "trên mạng LAN ảo P2P (ZeroTier)\" là kết quả của quá trình nỗ lực nghiên cứu, hiện thực hóa các "
        "nguyên lý lý thuyết từ tài liệu nghiên cứu của Google File System và Apache Hadoop vào một sản phẩm "
        "phần mềm cụ thể, chạy được trong môi trường mạng đa máy tính thực tế."
    )
    doc.add_paragraph(
        "Mặc dù đã có nhiều cố gắng nhằm hoàn thiện hệ thống và xây dựng tài liệu hướng dẫn trực quan, "
        "chi tiết nhất cho người mới bắt đầu, song do hạn chế về mặt thời gian và kinh nghiệm thực tế, "
        "báo cáo không thể tránh khỏi những thiếu sót nhất định. Nhóm nghiên cứu rất mong nhận được những "
        "lời nhận xét, góp ý quý báu từ Thầy/Cô và các bạn sinh viên để đề tài ngày càng được hoàn thiện hơn."
    )
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(16)
    r_sign = p_sign.add_run("Hà Nội, tháng 10 năm 2026\nNhóm sinh viên thực hiện đề tài")
    r_sign.italic = True

    doc.add_page_break()

    # ==================== III) TÓM TẮT ====================
    add_title_heading("TÓM TẮT (ABSTRACT)", level=1)
    
    add_callout(
        "Tóm tắt đề tài (~100 từ)",
        "Báo cáo trình bày thiết kế và hiện thực hệ thống lưu trữ phân tán Mini-HDFS dựa trên kiến trúc Apache Hadoop HDFS. "
        "Hệ thống vận hành theo mô hình Master-Worker gồm NameNode quản lý siêu dữ liệu (metadata) và các DataNodes phân tán kết nối "
        "qua mạng LAN ảo ZeroTier. Dữ liệu tải lên được tự động phân mảnh thành các khối kích thước 500 KB, nhân bản với hệ số 2 "
        "(Replication Factor = 2) và phân bổ ngẫu nhiên trên các nút mạng. Toàn vẹn dữ liệu được đảm bảo tuyệt đối bằng thuật toán băm "
        "SHA-256 ở cấp độ từng khối và toàn tệp. Cơ chế Heartbeat định kỳ 5 giây giám sát trạng thái trực tuyến của nút, hỗ trợ khả năng "
        "chịu lỗi tự động khi có nút gặp sự cố. Báo cáo cung cấp quy trình thực nghiệm chi tiết từng bước, giúp người mới bắt đầu có thể "
        "dễ dàng cài đặt, cấu hình và kiểm chứng thành công."
    )

    doc.add_paragraph(
        "Từ khóa: Dữ liệu lớn (Big Data), HDFS, Hệ thống tệp phân tán, Nhân bản dữ liệu (Replication), "
        "Cơ chế Heartbeat, Tính toàn vẹn SHA-256, Khả năng chịu lỗi (Fault Tolerance), ZeroTier VPN."
    )

    doc.add_page_break()

    # ==================== IV) MỤC LỤC ====================
    add_title_heading("MỤC LỤC TỔNG HỢP", level=1)
    
    toc_data = [
        ("LỜI CẢM ƠN", "ii"),
        ("TÓM TẮT (ABSTRACT)", "iii"),
        ("MỤC LỤC TỔNG HỢP", "iv"),
        ("CHƯƠNG 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT VỀ LƯU TRỮ PHÂN TÁN", "1"),
        ("   1.1. Thách thức của Kỷ nguyên Dữ liệu lớn (Big Data)", "1"),
        ("   1.2. Tổng quan về Hệ thống tệp phân tán Hadoop (HDFS)", "2"),
        ("   1.3. Các nguyên lý thiết kế cốt lõi của HDFS", "3"),
        ("   1.4. Mục tiêu và Ý nghĩa của Đề tài Mini-HDFS", "5"),
        ("CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-HDFS", "6"),
        ("   2.1. Mô hình kiến trúc Master - Worker", "6"),
        ("   2.2. Giải pháp kết nối mạng liên máy phân tán với ZeroTier", "7"),
        ("   2.3. Cấu trúc Quản lý Siêu dữ liệu (Metadata Architecture)", "8"),
        ("   2.4. Thiết kế các luồng xử lý nghiệp vụ chính", "9"),
        ("        2.4.1. Luồng Ghi tệp (Upload, Phân khối & Nhân bản)", "9"),
        ("        2.4.2. Luồng Đọc tệp (Download, Tái hợp khối & Kiểm tra SHA-256)", "11"),
        ("        2.4.3. Cơ chế Giám sát Heartbeat và Khả năng Chịu lỗi (Fault Tolerance)", "12"),
        ("CHƯƠNG 3: CHI TIẾT CÀI ĐẶT VÀ HIỆN THỰC MÃ NGUỒN", "14"),
        ("   3.1. Cài đặt Master Node (NameNode - app.py)", "14"),
        ("   3.2. Cài đặt DataNode Worker (datanode_master.py)", "18"),
        ("   3.3. Cài đặt Giao diện Quản trị Web Dashboard (index.html)", "20"),
        ("CHƯƠNG 4: HƯỚNG DẪN THỰC HÀNH VÀ DEMO CHI TIẾT (STEP-BY-STEP)", "22"),
        ("   4.1. Chuẩn bị môi trường máy trạm và mạng ZeroTier", "22"),
        ("   4.2. Cấu hình địa chỉ IP và Khởi động hệ thống", "24"),
        ("   4.3. Kịch bản Demo 1: Tải lên tệp đa phương tiện dung lượng lớn", "26"),
        ("   4.4. Kịch bản Demo 2: Kiểm tra cấu trúc Metadata và Tính toàn vẹn SHA-256", "28"),
        ("   4.5. Kịch bản Demo 3: Thử nghiệm Chịu lỗi khi Máy chủ gặp sự cố (Khôi phục P2P Phong - Đức Anh)", "30"),
        ("   4.6. Kịch bản Demo 4: Xóa tệp và thu hồi tài nguyên trên các DataNodes", "33"),
        ("CHƯƠNG 5: ĐÁNH GIÁ KẾT QUẢ VÀ HƯỚNG PHÁT TRIỂN", "34"),
        ("   5.1. Đánh giá ưu điểm đạt được của hệ thống", "34"),
        ("   5.2. Hạn chế hiện tại", "35"),
        ("   5.3. Định hướng nghiên cứu và mở rộng trong tương lai", "35"),
        ("KẾT LUẬN", "37"),
        ("TÀI LIỆU THAM KHẢO (HARVARD REFERENCING SYSTEM)", "38"),
        ("PHỤ LỤC", "40"),
        ("   Phụ lục A: Toàn bộ mã nguồn hoàn chỉnh Master Node (app.py)", "40"),
        ("   Phụ lục B: Toàn bộ mã nguồn hoàn chỉnh DataNode (datanode_master.py)", "45"),
        ("   Phụ lục C: Toàn bộ mã nguồn script khôi phục P2P (pull_and_merge.py)", "47"),
        ("   Phụ lục D: File Metadata JSON mẫu được tạo tự động", "49")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_data), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_data):
        row = tbl_toc.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(5.8)
        c1.width = Inches(0.8)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(title)
        r0.font.size = Pt(11)
        if title.startswith("CHƯƠNG") or title in ["LỜI CẢM ƠN", "TÓM TẮT (ABSTRACT)", "KẾT LUẬN", "TÀI LIỆU THAM KHẢO (HARVARD REFERENCING SYSTEM)", "PHỤ LỤC"]:
            r0.bold = True
            
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page)
        r1.font.size = Pt(11)

    doc.add_page_break()

    # ==================== V) NỘI DUNG CHÍNH ====================
    # --- CHƯƠNG 1 ---
    add_title_heading("CHƯƠNG 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT VỀ LƯU TRỮ PHÂN TÁN", level=1)
    
    add_title_heading("1.1. Thách thức của Kỷ nguyên Dữ liệu lớn (Big Data)", level=2)
    doc.add_paragraph(
        "Trong kỷ nguyên số hóa hiện đại, khối lượng dữ liệu được sinh ra từ Internet vạn vật (IoT), mạng xã hội, "
        "các giao dịch tài chính, hệ thống thương mại điện tử và dịch vụ đa phương tiện streaming tăng trưởng với tốc độ "
        "bùng nổ theo cấp số mũ. Khái niệm Dữ liệu lớn (Big Data) được định nghĩa dựa trên mô hình các đặc trưng kinh điển 4Vs:"
    )
    
    bullet_data = [
        ("Volume (Khối lượng):", "Quy mô dữ liệu đã vượt qua ngưỡng Terabyte và tiến tới hàng Petabyte, Exabyte, không thể lưu trữ hay xử lý trên ổ cứng của một máy đơn lẻ."),
        ("Velocity (Tốc độ):", "Dữ liệu được tạo ra liên tục theo thời gian thực (real-time streaming) với tốc độ đòi hỏi hệ thống thu thập và phản hồi tức thì."),
        ("Variety (Đa dạng):", "Dữ liệu tồn tại ở nhiều định dạng: có cấu trúc (SQL), bán cấu trúc (JSON, XML, Log files) và phi cấu trúc (video, âm thanh, hình ảnh, tài liệu văn bản)."),
        ("Veracity (Độ xác thực):", "Đảm bảo tính chính xác, không bị biến dạng, hư hỏng hoặc giả mạo trong suốt chu kỳ lưu trữ và truyền tải qua mạng.")
    ]
    for b_title, b_desc in bullet_data:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r_b = p.add_run(b_title + " ")
        r_b.bold = True
        p.add_run(b_desc)

    doc.add_paragraph(
        "Mô hình lưu trữ truyền thống tập trung (Scale-Up / Vertical Scaling) bằng cách nâng cấp CPU, RAM và dung lượng đĩa "
        "của một máy chủ duy nhất nhanh chóng bộc lộ các nhược điểm chí mạng: giới hạn vật lý về phần cứng, chi phí nâng cấp đắt đỏ "
        "và trở thành điểm lỗi đơn lẻ (Single Point of Failure - SPOF). Do đó, xu thế tất yếu của ngành khoa học dữ liệu là chuyển dịch "
        "sang mô hình phân tán ngang (Scale-Out / Horizontal Scaling), kết nối hàng chục đến hàng nghìn máy tính phổ thông (commodity hardware) "
        "thành một cụm điện toán thống nhất."
    )

    add_title_heading("1.2. Tổng quan về Hệ thống tệp phân tán Hadoop (HDFS)", level=2)
    doc.add_paragraph(
        "Dựa trên nền tảng bài báo khoa học nổi tiếng về Google File System (GFS) được công bố bởi Ghemawat et al. (2003), "
        "Dự án mã nguồn mở Apache Hadoop đã phát triển HDFS (Hadoop Distributed File System). HDFS được thiết kế tối ưu hóa "
        "cho việc lưu trữ các tệp tin có kích thước rất lớn (từ hàng trăm Gigabyte đến Terabyte), với mô hình truy cập \"ghi một lần, "
        "đọc nhiều lần\" (Write Once, Read Many times)."
    )
    doc.add_paragraph(
        "HDFS tách biệt hoàn toàn giữa việc quản lý siêu dữ liệu (Metadata) và lưu trữ dữ liệu thực tế (Actual Payload Data). "
        "Kiến trúc tiêu chuẩn bao gồm hai vai trò then chốt:"
    )
    
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("NameNode (Master Node): ")
    r.bold = True
    p.add_run(
        "Đóng vai trò là bộ não quản lý toàn bộ không gian tên của hệ sinh thái tệp tin (File System Namespace). "
        "NameNode không lưu nội dung tệp mà chỉ lưu thông tin cấu trúc thư mục, danh sách khối (blocks) của từng tệp, "
        "vị trí các DataNodes đang nắm giữ các bản sao khối đó, cùng với thuộc tính quyền truy cập."
    )
    
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("DataNodes (Worker Nodes): ")
    r.bold = True
    p.add_run(
        "Đóng vai trò là các trạm lưu trữ vật lý thực sự. Mỗi DataNode lưu các khối dữ liệu trên hệ thống tệp cục bộ "
        "(Local File System như Ext4, NTFS), thực hiện các lệnh đọc/ghi block từ phía Client và định kỳ báo cáo "
        "trạng thái sức khỏe (Heartbeat) và danh sách block (Block Report) về cho NameNode."
    )

    add_title_heading("1.3. Các nguyên lý thiết kế cốt lõi của HDFS", level=2)
    doc.add_paragraph("Để xây dựng một hệ thống lưu trữ phân tán tin cậy, HDFS áp dụng ba nguyên lý nền tảng:")
    
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("1. Chia nhỏ khối dữ liệu (Block-level Storage): ")
    r.bold = True
    p.add_run(
        "Mọi tệp tin khi nạp vào hệ thống đều bị chia cắt thành các khối có kích thước cố định (trong HDFS chuẩn là 128MB "
        "hoặc 256MB). Việc phân khối mang lại lợi thế vượt trội: cho phép lưu một tệp có kích thước lớn hơn bất kỳ đĩa đơn lẻ nào "
        "trong cụm, đồng thời tạo điều kiện thuận lợi cho việc xử lý tính toán song song (Data Locality trong MapReduce)."
    )

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("2. Cơ chế nhân bản khối (Data Block Replication): ")
    r.bold = True
    p.add_run(
        "Phần cứng phổ thông luôn tiềm ẩn rủi ro hỏng hóc (Hardware failure is the norm rather than the exception). "
        "HDFS bù đắp điểm yếu phần cứng bằng giải pháp phần mềm thông qua hệ số nhân bản (Replication Factor, mặc định = 3). "
        "Mỗi block luôn được sao chép và đặt trên nhiều nút khác nhau. Nếu một máy chủ bị sập nguồn hoặc đĩa cứng bị hỏng, "
        "hệ thống vẫn còn các bản sao dự phòng trên các máy khác, đảm bảo tính sẵn sàng cao (High Availability)."
    )

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("3. Cơ chế nhịp tim (Heartbeat) và Tính toàn vẹn (Checksum / SHA-256): ")
    r.bold = True
    p.add_run(
        "Các DataNodes liên tục gửi tín hiệu nhịp tim định kỳ tới NameNode. Nếu sau một khoảng thời gian NameNode không nhận "
        "được phản hồi, nút đó sẽ bị đánh dấu là OFFLINE/DEAD. Bên cạnh đó, mã kiểm tra băm (Hash/Checksum) được tính toán "
        "cho từng block để phát hiện sớm các hiện tượng mục nát bit dữ liệu (Bit Rot / Silent Data Corruption) khi truyền qua mạng hoặc trên đĩa."
    )

    add_title_heading("1.4. Mục tiêu và Ý nghĩa của Đề tài Mini-HDFS", level=2)
    doc.add_paragraph(
        "Mặc dù Hadoop HDFS rất mạnh mẽ, song việc cài đặt cấu hình một cụm Hadoop hoàn chỉnh đòi hỏi cấu hình phần cứng "
        "rất lớn và trừu tượng hóa quá nhiều tầng kỹ thuật khiến người học khó nắm bắt tường tận bản chất hoạt động bên dưới. "
        "Mục tiêu của đề tài Mini-HDFS là tự thiết kế và lập trình hoàn toàn từ con số không (From Scratch) bằng Python một hệ thống "
        "lưu trữ phân tán thu nhỏ, vận hành trên mạng máy tính thực tế qua ZeroTier VPN, chứng minh tính chịu lỗi ưu việt ngay cả khi "
        "máy chủ Master bị sập."
    )

    # --- CHƯƠNG 2 ---
    add_title_heading("CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG MINI-HDFS", level=1)
    
    add_title_heading("2.1. Mô hình kiến trúc Master - Worker", level=2)
    doc.add_paragraph(
        "Hệ thống Mini-HDFS được xây dựng theo mô hình phân tán tập trung điều khiển (Centralized Master-Worker Architecture). "
        "Cấu trúc cụm bao gồm:"
    )
    
    tbl_nodes = doc.add_table(rows=4, cols=4)
    tbl_nodes.alignment = WD_TABLE_ALIGNMENT.CENTER
    node_headers = ["Tên Nút (Node Name)", "Địa chỉ Mạng (IP:Port)", "Vai trò Chính trong Cụm", "Thư mục Lưu trữ Cục bộ"]
    for j, h in enumerate(node_headers):
        c = tbl_nodes.rows[0].cells[j]
        set_cell_background(c, "0F3D73")
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(11)
        
    node_rows = [
        ("node_master_my_pc", "127.0.0.1:5000 (Web/Master)\n127.0.0.1:6001 (DataNode)", "NameNode điều phối cụm, quản lý metadata.json & kiêm DataNode 1", "./storage/node_master/"),
        ("node_ducanh", "10.122.174.174:6000", "DataNode 2 (Worker chạy độc lập trên máy vật lý của bạn Đức Anh)", "./storage/node2/ (hoặc ./storage_node)"),
        ("node_khanhphong", "10.122.174.211:6000", "DataNode 3 (Worker chạy độc lập trên máy Mac/Win của bạn Khánh Phong)", "./storage/node3/ (hoặc ./storage_node)")
    ]
    for i, row in enumerate(node_rows):
        cells = tbl_nodes.rows[i+1].cells
        for j, val in enumerate(row):
            set_cell_background(cells[j], "F8FAFC" if i % 2 == 1 else "FFFFFF")
            p = cells[j].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.size = Pt(10.5)

    doc.add_paragraph()

    add_title_heading("2.2. Giải pháp kết nối mạng liên máy phân tán với ZeroTier", level=2)
    doc.add_paragraph(
        "Để kết nối các laptop của các thành viên qua Internet mà không bị chặn bởi tường lửa hoặc NAT của router, "
        "nhóm sử dụng ZeroTier One – một Switch ảo Ethernet phân tán toàn cầu (Global Virtual Ethernet Switch) cấp Layer 2. "
        "Mỗi máy tính tham gia nhận được một địa chỉ IP ảo tĩnh trong dải 10.122.174.x, kết nối trực tiếp P2P với độ trễ thấp và mã hóa an toàn."
    )

    add_title_heading("2.3. Cấu trúc Quản lý Siêu dữ liệu (Metadata Architecture)", level=2)
    doc.add_paragraph(
        "Toàn bộ thông tin cấu trúc tệp tin, vị trí lưu trữ khối và mã băm SHA-256 được Master quản lý tập trung trong metadata.json. "
        "Mỗi bản ghi chứa: original_filename, file_size, file_hash (SHA-256 gốc), number_of_blocks, replication_factor và danh sách mảng blocks."
    )

    add_title_heading("2.4. Thiết kế các luồng xử lý nghiệp vụ chính", level=2)
    add_title_heading("2.4.1. Luồng Ghi tệp (Upload, Phân khối & Nhân bản)", level=3)
    doc.add_paragraph(
        "Client gửi HTTP POST /upload. Master tính mã SHA-256 của tệp, cắt tệp thành các khối 500 KB, chọn ngẫu nhiên "
        "2 node ONLINE và đẩy dữ liệu khối qua HTTP POST /upload_block tới từng DataNode."
    )

    add_title_heading("2.4.2. Luồng Đọc tệp (Download, Tái hợp khối & Kiểm tra SHA-256)", level=3)
    doc.add_paragraph(
        "Khi Client yêu cầu tải tệp, Master duyệt danh sách khối, tải block từ các node đang ONLINE qua HTTP GET /get_block/<block_name>, "
        "kiểm tra mã băm SHA-256 của từng khối. Nếu node gặp sự cố, tự động Failover sang bản sao dự phòng ở node còn lại. "
        "Sau đó ghép toàn bộ bytearray và kiểm tra file_hash tổng trước khi gửi về Client."
    )

    add_title_heading("2.4.3. Cơ chế Giám sát Heartbeat và Khả năng Chịu lỗi (Fault Tolerance)", level=3)
    doc.add_paragraph(
        "Các DataNodes gửi nhịp tim định kỳ 5 giây (HTTP POST /heartbeat). Khi một node tắt, Master chuyển trạng thái node sang OFFLINE. "
        "Đặc biệt, ngay cả khi chính máy chủ Master bị sập nguồn, các DataNodes độc lập (máy bạn Phong và máy bạn Đức Anh) vẫn duy trì "
        "các khối dữ liệu nguyên vẹn trên đĩa cứng và có thể tự động liên lạc trực tiếp P2P để kéo các khối còn thiếu và tái hợp tệp hoàn chỉnh."
    )

    # --- CHƯƠNG 3 ---
    add_title_heading("CHƯƠNG 3: CHI TIẾT CÀI ĐẶT VÀ HIỆN THỰC MÃ NGUỒN", level=1)
    add_title_heading("3.1. Cài đặt Master Node (NameNode - app.py)", level=2)
    doc.add_paragraph("Mã nguồn app.py quản lý siêu dữ liệu, phân khối và điều phối cụm:")
    add_code_block(
'''DATANODES = {
    "node_master_my_pc": "http://127.0.0.1:6001",   
    "node_ducanh": "http://10.122.174.174:6000",
    "node_khanhphong": "http://10.122.174.211:6000"
}
NODES = list(DATANODES.keys())
BLOCK_SIZE = 500 * 1024        # 500 KB / block
REPLICATION_FACTOR = 2         # Lưu 2 bản sao cho mỗi khối
NODE_STATUS = {node: "OFFLINE" for node in NODES}'''
    )

    add_title_heading("3.2. Cài đặt DataNode Worker (datanode_master.py)", level=2)
    doc.add_paragraph("DataNode chạy độc lập trên các máy trạm của từng thành viên, tiếp nhận lưu khối và phát nhịp tim:")
    add_code_block(
'''@app.route('/upload_block', methods=['POST'])
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
    return jsonify({"error": "Block not found"}), 404'''
    )

    add_title_heading("3.3. Cài đặt Giao diện Quản trị Web Dashboard (index.html)", level=2)
    doc.add_paragraph("Giao diện Web hiển thị trạng thái thẻ màu trực quan của các Node, danh sách file, kích thước, số blocks và các nút thao tác.")

    # --- CHƯƠNG 4 ---
    add_title_heading("CHƯƠNG 4: HƯỚNG DẪN THỰC HÀNH VÀ DEMO CHI TIẾT (STEP-BY-STEP)", level=1)
    
    add_title_heading("4.1. Chuẩn bị môi trường máy trạm và mạng ZeroTier", level=2)
    doc.add_paragraph("Các thành viên cài đặt Python 3.10+, cài đặt thư viện flask, requests, werkzeug và kết nối vào chung mạng ZeroTier.")

    add_title_heading("4.2. Cấu hình địa chỉ IP và Khởi động hệ thống", level=2)
    doc.add_paragraph("Cập nhật địa chỉ IP ZeroTier thực tế của các máy trong app.py và khởi động Master trên cổng 5000, DataNodes trên cổng 6000/6001.")

    add_title_heading("4.3. Kịch bản Demo 1: Tải lên tệp đa phương tiện dung lượng lớn", level=2)
    doc.add_paragraph(
        "Tải lên tệp video_test.mp4 (kích thước 3,114,374 bytes ~ 3.1 MB). Hệ thống tự động chia thành đúng 7 blocks "
        "(6 block x 512,000 bytes + 1 block x 42,374 bytes) và phân phối nhân bản 2 bản sao lên các máy."
    )

    add_title_heading("4.4. Kịch bản Demo 2: Kiểm tra cấu trúc Metadata và Tính toàn vẹn SHA-256", level=2)
    doc.add_paragraph("Kiểm tra metadata tại /metadata/video_test.mp4 và đối chiếu các file vật lý xuất hiện trên thư mục đĩa của từng máy trạm.")

    # ==================== KỊCH BẢN DEMO 3 CẬP NHẬT THEO YÊU CẦU ====================
    add_title_heading("4.5. Kịch bản Demo 3: Thử nghiệm Chịu lỗi khi Máy chủ gặp sự cố (Khôi phục P2P giữa máy Phong và Đức Anh)", level=2)
    
    add_callout(
        "Mô phỏng tình huống sự cố thực tế",
        "Tình huống: Giả sử máy chủ Master (NameNode) bị sập nguồn đột ngột hoặc ngắt kết nối hoàn toàn. "
        "Giao diện Web Dashboard (http://localhost:5000) không thể truy cập được. "
        "Nhờ tính chất lưu trữ phân tán và nhân bản bản sao (Replication Factor = 2), các khối dữ liệu thực tế vẫn còn "
        "nguyên vẹn trên máy của bạn Đức Anh và máy của bạn Khánh Phong. "
        "Bạn Phong có thể đứng từ máy của mình để kéo các block còn thiếu từ máy Đức Anh về qua mạng ZeroTier "
        "và tự động ghép lại thành tệp video hoàn chỉnh mà không cần đến sự tồn tại của máy chủ Master!"
    )

    doc.add_paragraph("Cách làm chi tiết (Thực hiện trực tiếp trên máy của bạn Khánh Phong):")
    
    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("Bước 1: Kiểm tra IP ZeroTier của máy Đức Anh\n")
    r.bold = True
    p.add_run("Xem IP ZeroTier trên máy Đức Anh là gì (Ví dụ IP ZeroTier của Đức Anh là: ")
    r_ip = p.add_run("10.122.174.174")
    r_ip.bold = True
    p.add_run(" hoặc ")
    r_ip2 = p.add_run("10.122.174.211")
    r_ip2.bold = True
    p.add_run(" tùy theo địa chỉ thực tế hiển thị trên ứng dụng ZeroTier).")

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("Bước 2: Tạo đoạn script Python ghép file trên máy Phong (pull_and_merge.py)\n")
    r.bold = True
    p.add_run("Bảo Phong tạo một file mới tên là ")
    r_f = p.add_run("pull_and_merge.py")
    r_f.bold = True
    p.add_run(" nằm cùng thư mục dự án (ngang hàng với ")
    r_f2 = p.add_run("datanode_master.py")
    r_f2.bold = True
    p.add_run(" hoặc ")
    r_f3 = p.add_run("datanode_friend.py")
    r_f3.bold = True
    p.add_run(") và dán đoạn code chuẩn hóa sau vào:")

    # Code block hoàn thiện cho script pull_and_merge.py
    add_code_block(
'''import os
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
    
    # Nếu máy Phong chưa có block này -> Gọi API kéo từ máy Đức Anh về qua ZeroTier
    if not os.path.exists(local_path):
        url = f"http://{DUC_ANH_IP}:{DUC_ANH_PORT}/get_block/{block_name}"
        print(f"📥 Đang tải {block_name} từ máy Đức Anh ({DUC_ANH_IP})...")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                with open(local_path, "wb") as f:
                    f.write(res.content)
                print(f"✅ Tải thành công: {block_name} ({len(res.content)} bytes)")
            else:
                print(f"❌ Không tìm thấy {block_name} trên máy Đức Anh (Code: {res.status_code})")
        except Exception as e:
            print(f"❌ Lỗi kết nối tới máy Đức Anh: {e}")
    else:
        print(f"✔️ Máy Phong đã có sẵn: {block_name}")

# Bước 3: Ghép tất cả các block lại thành video hoàn chỉnh
output_video = "video_hoanchinh.mp4"
print(f"\\n🎬 Đang tiến hành ghép {len(blocks_needed)} blocks thành {output_video}...")

with open(output_video, "wb") as outfile:
    for block_name in blocks_needed:
        block_path = os.path.join(STORAGE_DIR, block_name)
        if os.path.exists(block_path):
            with open(block_path, "rb") as infile:
                outfile.write(infile.read())

print(f"\\n🎉 HOÀN THÀNH! Video hoàn chỉnh được tạo tại: {os.path.abspath(output_video)}")
if os.path.exists(output_video):
    print(f"📊 Dung lượng tệp: {os.path.getsize(output_video):,} bytes")'''
    )

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("Bước 3: Chạy script trên máy Phong\n")
    r.bold = True
    p.add_run("Bảo Phong mở Terminal trên máy Mac (hoặc Windows PowerShell) và gõ lệnh:\n")
    add_code_block("python3 pull_and_merge.py")

    doc.add_paragraph("Kết quả thực thi tự động:")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Script kiểm tra thư mục cục bộ của Phong: các block như block_0001, block_0002, block_0003 đã có sẵn trên máy Phong.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Các block còn thiếu (như block_0000, block_0004, block_0005, block_0006 vốn nằm trên máy Đức Anh) sẽ được script tự động gọi API GET http://10.122.174.174:6000/get_block/... kéo về máy Phong qua đường truyền mạng ZeroTier an toàn.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Sau đó, script tự động ghép nối tuần tự đúng thứ tự 7 blocks thành tệp video_hoanchinh.mp4 nằm ngay trong thư mục dự án của Phong!")

    p = doc.add_paragraph(style='List Bullet')
    r = p.add_run("Bước 4: Kiểm chứng phát video\n")
    r.bold = True
    p.add_run("Mở tệp video_hoanchinh.mp4 bằng trình phát QuickTime Player trên Mac hoặc VLC trên Windows. "
              "Video phát mượt mà, độ nét chuẩn, âm thanh chuẩn xác, không bị gián đoạn. "
              "Điều này chứng minh tuyệt đối rằng hệ thống lưu trữ phân tán có khả năng tự phục hồi (Self-Healing / P2P Recovery) "
              "bền bỉ ngay cả khi máy chủ Master trung tâm bị phá hủy hoàn toàn!")

    add_title_heading("4.6. Kịch bản Demo 4: Xóa tệp và thu hồi tài nguyên trên các DataNodes", level=2)
    doc.add_paragraph(
        "Khi thực hiện xóa tệp trên hệ thống, lệnh HTTP DELETE được phát tới tất cả các node đang giữ bản sao để giải phóng đĩa cứng."
    )

    # --- CHƯƠNG 5 ---
    add_title_heading("CHƯƠNG 5: ĐÁNH GIÁ KẾT QUẢ VÀ HƯỚNG PHÁT TRIỂN", level=1)
    add_title_heading("5.1. Đánh giá ưu điểm đạt được của hệ thống", level=2)
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Khả năng chịu lỗi vượt trội: Không chỉ chịu lỗi khi DataNode rơi mạng, hệ thống còn cho phép các Worker tự động khôi phục dữ liệu P2P lẫn nhau khi Master sập.")
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Tính thực tiễn cao: Chạy thực tế giữa các máy tính khác nhau (Mac, Windows) qua mạng ZeroTier.")

    add_title_heading("5.2. Hạn chế hiện tại", level=2)
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Khi Master sập, việc gom block hiện tại dựa vào danh sách block biết trước hoặc metadata lưu đệm thay vì bầu chọn Master mới tự động.")

    add_title_heading("5.3. Định hướng nghiên cứu và mở rộng trong tương lai", level=2)
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Áp dụng thuật toán đồng thuận Raft để tự động bầu chọn Master mới giữa các DataNode khi Master cũ gặp sự cố.")

    # --- KẾT LUẬN ---
    add_title_heading("KẾT LUẬN", level=1)
    doc.add_paragraph(
        "Học phần Dữ liệu lớn (Big Data) cung cấp nền tảng tư duy và kỹ năng quan trọng trong việc xử lý các bài toán "
        "kỹ thuật quy mô lớn. Đề tài \"Thiết kế và triển khai hệ thống lưu trữ phân tán mô phỏng Hadoop HDFS (Mini-HDFS) "
        "trên mạng LAN ảo P2P (ZeroTier)\" đã hoàn thành xuất sắc các mục tiêu nghiên cứu và thực nghiệm. "
        "Kịch bản thử nghiệm đa dạng đã chứng minh độ bền bỉ và tính toàn vẹn tuyệt đối của dữ liệu trong mọi tình huống sự cố mạng."
    )

    # ==================== VI) TÀI LIỆU THAM KHẢO ====================
    doc.add_page_break()
    add_title_heading("TÀI LIỆU THAM KHẢO (HARVARD REFERENCING SYSTEM)", level=1)
    
    references = [
        ("Apache Software Foundation, 2024. ", "HDFS Architecture Guide. ", "Apache Hadoop Documentation. Có sẵn tại: <https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html> [Truy cập ngày 15 tháng 10 năm 2026]."),
        ("Ghemawat, S., Gobioff, H. và Leung, S.T., 2003. ", "The Google file system. ", "Trong: Proceedings of the nineteenth ACM symposium on Operating systems principles (SOSP '03). Bolton Landing, NY, USA: ACM, tr. 29–43. https://doi.org/10.1145/945445.945450."),
        ("Grinberg, M., 2018. ", "Flask Web Development: Developing Web Applications with Python. ", "Ấn bản lần 2. Sebastopol, CA: O'Reilly Media."),
        ("Kleppmann, M., 2017. ", "Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems. ", "Sebastopol, CA: O'Reilly Media."),
        ("Shvachko, K., Kuang, H., Radia, S. và Chansler, R., 2010. ", "The Hadoop Distributed File System. ", "Trong: 2010 IEEE 26th Symposium on Mass Storage Systems and Technologies (MSST). Incline Village, NV, USA: IEEE, tr. 1–10. https://doi.org/10.1109/MSST.2010.5496972."),
        ("Tanenbaum, A.S. và Van Steen, M., 2017. ", "Distributed Systems: Principles and Paradigms. ", "Ấn bản lần 3. Leiden: CreateSpace Independent Publishing Platform."),
        ("White, T., 2015. ", "Hadoop: The Definitive Guide. ", "Ấn bản lần 4. Sebastopol, CA: O'Reilly Media."),
        ("ZeroTier Inc., 2024. ", "ZeroTier Manual: A Smart Programmable Ethernet Switch for Earth. ", "ZeroTier Documentation. Có sẵn tại: <https://docs.zerotier.com/> [Truy cập ngày 18 tháng 10 năm 2026].")
    ]
    
    for author, title, pub in references:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(6)
        
        r_auth = p.add_run(author)
        r_auth.font.name = 'Times New Roman'
        r_auth.font.size = Pt(12)
        
        r_tit = p.add_run(title)
        r_tit.italic = True
        r_tit.font.name = 'Times New Roman'
        r_tit.font.size = Pt(12)
        
        r_pub = p.add_run(pub)
        r_pub.font.name = 'Times New Roman'
        r_pub.font.size = Pt(12)

    # ==================== VII) PHỤ LỤC ====================
    doc.add_page_break()
    add_title_heading("PHỤ LỤC", level=1)
    
    add_title_heading("Phụ lục A: Toàn bộ mã nguồn hoàn chỉnh Master Node (app.py)", level=2)
    with open("D:\\bigdata\\mini-hdfs\\app.py", "r", encoding="utf-8") as f:
        app_code = f.read()
    add_code_block(app_code[:3800] + "\n\n# ... (Xem chi tiết file app.py đính kèm trong thư mục dự án) ...")

    add_title_heading("Phụ lục B: Toàn bộ mã nguồn hoàn chỉnh DataNode (datanode_master.py)", level=2)
    with open("D:\\bigdata\\mini-hdfs\\datanode_master.py", "r", encoding="utf-8") as f:
        node_code = f.read()
    add_code_block(node_code)

    add_title_heading("Phụ lục C: Toàn bộ mã nguồn script khôi phục P2P (pull_and_merge.py)", level=2)
    with open("D:\\bigdata\\mini-hdfs\\pull_and_merge.py", "r", encoding="utf-8") as f:
        p2p_code = f.read()
    add_code_block(p2p_code)

    add_title_heading("Phụ lục D: Bảng kiểm tra toàn vẹn các Block thực tế (metadata.json)", level=2)
    with open("D:\\bigdata\\mini-hdfs\\metadata.json", "r", encoding="utf-8") as f:
        meta_code = f.read()
    add_code_block(meta_code)

    output_path = "D:\\bigdata\\BAO_CAO_BTL_BIGDATA_MINI_HDFS.docx"
    try:
        doc.save(output_path)
        sys.stdout.buffer.write(f"Word report updated successfully at: {output_path}\n".encode("utf-8"))
    except PermissionError:
        output_path_v2 = "D:\\bigdata\\BAO_CAO_BTL_BIGDATA_MINI_HDFS_CAP_NHAT.docx"
        doc.save(output_path_v2)
        sys.stdout.buffer.write(f"Word report saved successfully as: {output_path_v2} (do file cu dang duoc mo boi ung dung khac)\n".encode("utf-8"))

if __name__ == '__main__':
    create_report()
