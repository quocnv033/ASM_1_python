1. github dự án : https://github.com/quocnv033/ASM_1_python#

2. Dự án bao gồm
    AMS_1.py là file là mã nguồn
    text_file là folder chứa các file text để đọc dữ liệu
    expected_output là folder chứa các file text được tạo trong quá trình ghi dữ liệu output


3.Để chạy file .py trên VS code
    cần cài đặt Python 3.13 từ https://www.python.org/downloads/release/python-3130/

    mở Terminal trên VS code và gõ: 

    python -m pip install pandas

    để cài đặt thư viện pandas (nếu chưa có)

4. Mô tả dự án
    Đây là chương trình được xây dựng bằng Python nhằm hỗ trợ chấm điểm bài thi trắc nghiệm của học sinh.

Chương trình cho phép:

- Mở và đọc tệp dữ liệu chứa câu trả lời của học sinh.
- Kiểm tra tính hợp lệ của dữ liệu (định dạng mã sinh viên và số lượng câu trả lời).
- Chấm điểm tự động theo đáp án chuẩn.
- Thống kê kết quả của cả lớp, bao gồm:
  - Số học sinh đạt trên 80 điểm.
  - Điểm trung bình.
  - Điểm cao nhất và thấp nhất.
  - Miền giá trị của điểm.
  - Trung vị.
  - Các câu hỏi bị bỏ qua nhiều nhất.
  - Các câu hỏi bị trả lời sai nhiều nhất.
- Xuất kết quả chấm điểm của từng học sinh ra tệp `.txt`.

5. Công nghệ sử dụng

- **Python 3.13**
- **Pandas** (xử lý và đọc dữ liệu)
- **Regular Expression (re)** (kiểm tra định dạng mã sinh viên)
- **os** (làm việc với đường dẫn và quản lý tệp)
