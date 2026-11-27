# Dùng giao diện Class Pulse

Trong thư mục repo, cài phụ thuộc một lần bằng `python -m pip install -r requirements.txt`, sau đó
chạy `python run.py`. Mở địa chỉ **URL** mà Streamlit in ra trong trình duyệt. Nếu máy dùng
môi trường ảo trên Windows, thay `python` bằng `.\.venv\Scripts\python.exe`.

Nhập câu hỏi như **Ngày 5 lớp vướng gì?** và chọn **Tạo thẻ điểm nghẽn**. Có thể chọn câu gợi ý để
điền nhanh. Sau khi thẻ xuất hiện, cuộn xuống phần gợi ý AI; dòng cuối cho biết model và số token từ
lượt vừa chạy. Thẻ là bản nháp, giảng viên cần duyệt. Khi quay xong, nhấn Ctrl+C trong cửa sổ lệnh để dừng ứng dụng.

Để có kết quả AI thật, điền `.env` theo `docs/connect-model.md`. Nếu model báo HTTP 429 hoặc 503,
ứng dụng tự thử lại có giới hạn; khi vẫn lỗi, đợi rồi thử lại hoặc kiểm tra hạn mức. Lệnh chạy bộ
đánh giá có thể dùng `python run.py eval --try --wait 4` để giãn cách giữa các câu.

Nếu cần dùng dòng lệnh thay cho giao diện web: `python codebase/app.py --cli`.
