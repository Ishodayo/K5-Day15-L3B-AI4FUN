# Reflection — Duy

*Bản nháp để Duy xem lại và bổ sung trải nghiệm cá nhân trước khi nộp.*

1. **Vai trò và phần việc:** Sửa luồng gợi ý của Class Pulse trước lượt đánh giá thứ hai. Thay đổi nằm ở `codebase/agent.py`, ghi lại trong `spec.md` §10 và được kiểm tra bằng `tests/test_cp4_duy.py`.

2. **AI hỗ trợ:** Codex hỗ trợ sửa code, chạy các câu thử và rà soát đầu ra. Khi thử model thật, câu trả lời từng suy đoán về học viên từ đề ví dụ; phần này được sửa bằng cách không gửi số liệu thật kèm đề synthetic và thêm bước lọc đầu ra. Giảng viên vẫn cần duyệt nội dung vì bộ lọc không hiểu được mọi cách diễn đạt.

3. **Bài học từ B05:** Tín hiệu sai dồn 12/12 vào một đáp án cho thấy cần xem lại câu hỏi, nhưng không chứng minh đề gốc sai hay học viên hiểu sai nội dung nào. Đề synthetic giúp tạo ví dụ ôn tập, không thay thế được đề gốc làm căn cứ kết luận.
