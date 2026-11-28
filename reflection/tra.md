# Reflection — Phùng Quang Trà

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Phụ trách bằng chứng người dùng và chi phí. CP2–CP3: ghi phỏng vấn P1 (`evidence/interviews/P1.md`, commit `cca6fbd`), tổng hợp bằng chứng pain + khớp/lệch giả thuyết (`evidence/summary.md`, `evidence/hypothesis.md`), bảng impact 4 hướng ở `spec.md` §2 (≈ 25 giờ giảng viên / tháng, mỗi thừa số có nguồn TKB / data hoặc ghi *tự ước tính*) — PR #5 (`c128deb`).
   CP4: `cost/personas.yaml` (3 persona, 3 kịch bản 3 / 5 / 10 người, giá 3 model), chạy `python run.py simulate --rate-from eval/run-2.csv` → `cost/simulate-1.csv` (50 phiên, `gpt-5.4-nano`), điền `cost/cost-estimate.md` và `spec.md` §8 (commit `985436a`, `303ea39`, `609eec8`). Kết quả: $0.0020 / task thành công, $0.0274 / người / tháng ở kịch bản cơ sở.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   Dùng Claude Code trong VS Code để đối chiếu từng số bằng chứng với `data/review_stats.csv` và `data/struggle_by_module.csv` (vd 0/399 lượt sai có làm lại), soạn `personas.yaml`, tra giá model trên trang giá OpenAI và chạy lệnh mô phỏng.
   Chỗ phải chỉnh: AI có ước nhanh chi phí từ token lượt 1, mình không dùng số đó — số nộp lấy nguyên từ `cost/simulate-1-summary.md`. File giá `further-reading/model-prices.md` của repo đề không có trên máy nên giá lấy từ trang OpenAI, mình ghi nguồn + ngày xem và đánh dấu cần đối chiếu. Thừa số "25 phút / buổi" và "1 giảng viên / lớp" không có nguồn nên phải ghi *(tự ước tính)*, không để như số thật.
   Khi mình lỡ merge thẳng nhánh CP3 vào `main`, nhờ AI revert (`c09fb2c`) thay vì force-push rồi làm lại qua PR — từ đó luôn kiểm nhánh trước khi push.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   **B01** ("Ngày 1: lớp đang vướng ý nào, gợi ý tôi điều chỉnh bài giảng") đạt ở lượt 1 nhưng trượt ở lượt 2: thẻ vẫn đủ số 16/41, 9/16, 115/187, nhưng bộ lọc `_loc_synthetic` bỏ toàn bộ phần gợi ý vì model không bọc `[mã thẻ]` trong ngoặc vuông. Bản sửa nhắm vào B02/B05/B17/B18 lại làm hỏng 5 câu đang đạt → tổng 20/24 → 15/24.
   Nhìn từ phía chi phí: 9 câu theo ngày mà persona "giảng viên chỉ đọc thẻ" dùng (24/50 phiên mô phỏng) đi từ 7/9 xuống 3/9 — tệ hơn nhiều so với tỉ lệ chung 62% mà công thức chi phí / task đang dùng. Bài học: (1) đúng số chưa đủ, thẻ không có gợi ý thì giảng viên không dùng được; (2) sau mỗi lần sửa phải chạy lại trọn bộ câu thử, kể cả câu đang đạt; (3) với model rẻ như nano, chi phí gần như không đáng kể — thứ quyết định đáng làm hay không là chất lượng trên đúng loại câu người dùng hỏi nhiều nhất.
