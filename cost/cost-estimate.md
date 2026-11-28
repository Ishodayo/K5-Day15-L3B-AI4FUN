# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu, lấy từ `spec.md` §2. Nguồn: số buổi lấy từ TKB (thời khoá biểu AI20K Khoá V do BTC phát, Phase 1 05/11–28/11/2026: mỗi lớp 15 buổi lý thuyết); vai người phụ trách nhiều lớp từ phỏng vấn P1; số lượt / phiên và tỉ lệ *(tự ước tính)*.

  | Persona | Tỉ lệ | Phiên / người / tháng | Lượt hỏi / phiên | Hỏi gì |
  |---|---|---|---|---|
  | `gv_chi_doc_the` — giảng viên chỉ đọc thẻ tự động 21:00 | 0,4 | 15 (1 / buổi lý thuyết — TKB) | 1 | câu theo ngày học trong `eval/benchmark.csv` |
  | `gv_hoi_tiep` — giảng viên hỏi tiếp theo mã câu | 0,4 | 15 (TKB) | 3 *(tự ước tính)* | ngẫu nhiên câu `thuong` + `kho` |
  | `phu_trach_nhieu_lop` — người phụ trách học thuật (vai P1) | 0,2 | 60 (4 lớp × 15 buổi — TKB) | 2 *(tự ước tính)* | ngẫu nhiên câu `thuong` + `kho` |

- **Số người dùng thật** 3 kịch bản (người dùng = giảng viên phụ trách buổi lý thuyết + người phụ trách học thuật): thấp **3** (chỉ 2 lớp L3) · cơ sở **5** (4 lớp Khoá V: 4 giảng viên + 1 người phụ trách) · cao **10** (2 khoá song song, 8 lớp). Nguồn: số lớp từ TKB; 1 giảng viên / lớp, 1 người phụ trách / 4 lớp và kịch bản 2 khoá song song *(tự ước tính — TKB không ghi tên giảng viên)*.
- **Giá** 3 mức model, USD / 1 triệu token (vào · ra), bảng Standard ở https://developers.openai.com/api/docs/pricing, xem 28/11/2026: `gpt-5.4-nano` 0,20 · 1,25 · `gpt-5.4-mini` 0,75 · 4,50 · `gpt-5.4` 2,50 · 15,00. *(Lấy thẳng từ trang giá của OpenAI vì máy không có `further-reading/model-prices.md` của repo đề — cần đối chiếu nếu file đó có giá khác.)*
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` (lượt 2)
- Đo token trên model __, tính giá model __ và __

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
