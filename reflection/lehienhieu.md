# Reflection — Lê Hiền Hiếu

1. **Vai trò + Phần làm:**
- Phụ trách mảng dữ liệu và đánh giá (Data & Eval) của nhóm AI4FUN cho dự án Class Pulse.
- Tham gia khai thác dữ liệu pre-class để hoàn thiện `data/DATA_CARD.md`
- Xây dựng `data/question_bank.csv` (19 câu `synthetic` khớp `ref`/`lesson_id`/`kc_code`)
- Tạo `data/lesson_mapping.csv` ánh xạ mã bài học với tên thật trên pre-class và mở rộng `eval/benchmark.csv` từ 14 lên 24 câu (`B15–B24`, PR #6).
- Ở CP3-CP4, chạy và chấm cả 2 lượt đánh giá (`eval/run-1.csv`, `eval/run-2.csv`, `traces/run-1.jsonl`, `traces/run-2.jsonl`)
- Hoàn thiện hồ sơ `eval/report.md`, `eval/README.md` và cập nhật `spec.md` §7.

2. **AI hỗ trợ:**
- Dùng AI để rà soát các điểm thiếu sót của repo so với yêu cầu đề
- Tổng hợp khung đề ví dụ cho `data/question_bank.csv`
- Gợi ý kịch bản cho câu thử `B15–B24`
- Tạo `data/lesson_mapping.csv`
- Hỗ trợ đối chiếu chấm cột `pass` và soạn nháp báo cáo đánh giá.

 Tuy nhiên, cũng tự kiểm tra và sửa lại nhiều chỗ: 
- Đối chiếu tay toàn bộ 19 dòng `question_bank.csv` để gắn đúng nhãn `synthetic` và khóa ngoại
- Soi ảnh giao diện pre-class để phát hiện D03–D04 bị đảo thứ tự so với data BTC và gắn cờ chưa xác minh cho D09–D13
- Đồng thời tự rà từng output của `run-1.csv` và `run-2.csv` bằng `python run.py score` để bảo đảm chấm nhất quán và không lệch trace.

3. **Một câu thử trượt của nhóm và bài học được gì từ nó:** Câu `B02` (*"Ngày 3 lớp hiểu sai gì nhiều nhất?"*) trượt ở cả hai lượt vì hai lỗi hoàn toàn khác nhau: lượt 1 AI tự đoán sai nghĩa mã không dấu `d03-on-dung-dung-luc` ("dừng đúng lúc") thành *"dùng đúng lúc"*; sang lượt 2, khi thêm bộ lọc `_loc_synthetic` để chặn suy đoán, regex bắt buộc dấu ngoặc vuông `[mã_thẻ]` lại không khớp với output thực tế của `gpt-5.4-nano` nên code xoá sạch phần gợi ý AI (kéo toàn bộ 8/8 câu `thuong` trượt theo, tổng giảm từ 83% xuống 62%). Tôi học được rằng unit test cục bộ qua hết không đồng nghĩa model thật sẽ ra đúng định dạng — các bộ lọc hậu kiểm cần linh hoạt (hoặc dùng structured output) và luôn phải chạy lại full eval sau mỗi lần sửa để bắt sớm lỗi hồi quy.
