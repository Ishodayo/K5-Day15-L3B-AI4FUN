# Reflection — Nguyễn Thành Nam

1. **Vai trò + phần mình làm:**
   - Đội trưởng: điều phối, chia việc theo checkpoint (mỗi người làm trọn một phần), soát và nộp CP1–CP4.
   - Đào data điểm nghẽn: `evidence/count_review.py`, `evidence/count_struggle.py`, `evidence/data-mining.md` → `data/review_stats.csv`, `data/struggle_by_module.csv`.
   - Viết khung `codebase/agent.py` và `tools.py`: luồng cố định, 3 công cụ chỉ đọc, regex từ chối, lớp kiểm đầu ra.
   - Viết `spec.md` §0, §1, §3–§6, §9–§10, `docs/ai-usage.md`, slide `demo-slides.pdf`, `slides/demo-script.md`.
   - Cùng Trà phỏng vấn P1.
2. **AI hỗ trợ thế nào:**
   - Dùng Claude Code để viết script đếm, khung code, soạn spec và slide.
   - Phải sửa AI 3 chỗ:
     - Ngưỡng mẫu ban đầu là 20, nhiều ngày không còn câu nào đủ mẫu nên hạ xuống 10.
     - 208/453 dòng lab có `kc_code` trống, phải ghép bằng `lesson_id` + `lab_key`.
     - Bản đầu của lớp kiểm chỉ bắt số dạng x/N, phải thêm kiểm số %.
   - Trên slide, một câu AI đặt trong ngoặc kép như lời P1 thật ra là ý tóm tắt trong ghi chép. Mình đã đổi sang trích nguyên văn có trong `evidence/summary.md`.
   - Mọi số trên slide đều được đối chiếu lại với CSV đầu ra.
3. **Một câu thử trượt và bài học:**
   - **B01** đạt ở lượt 1 nhưng trượt ở lượt 2. Thẻ vẫn đủ số 16/41, 115/187, nhưng phần gợi ý AI bị `_loc_synthetic` bỏ vì model không in mã thẻ trong ngoặc vuông.
   - Lớp chặn an toàn càng chặt thì càng dễ chặn luôn cả câu trả lời đúng. Lỗi "bỏ quá tay" không lộ ra nếu chỉ thử tay mấy câu đang trượt.
   - Là người điều phối, lẽ ra mình phải bắt chạy lại cả 8 câu `thuong` (hoặc `eval --try`) trước khi chạy lượt 2 thật. Lần sau, mỗi bản sửa phải qua cả những câu đang đạt trước khi tính là một lượt có số.
