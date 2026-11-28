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
- **Tỉ lệ đạt** dùng để tính: 15/24 (62,5%) — lượt `run-2@20261128-101829` (lượt 2, `eval/run-2.csv`, model `gpt-5.4-nano`). Lượt 2 thấp hơn lượt 1 (20/24, 83%) — dùng đúng số lượt 2 theo phân công, không lấy lượt 1 cho đẹp.
- Đo token trên model **`gpt-5.4-nano`** (model nhóm dùng để build và chạy eval), tính giá **`gpt-5.4-nano`** (model chính — số báo cáo ở slide và `spec.md` §8) và `gpt-5.4-mini`, `gpt-5.4` (để so mức mạnh hơn). Hai model sau dùng chung số token đo trên nano.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-113444` · 50 phiên · seed 42 · model thật `gpt-5.4-nano` · 0/50 phiên lỗi · trace `traces/simulate-1.jsonl` · code ở commit `41c71e9` (đã gộp `main` `b141488`, cùng agent với lượt 2)

*(chép nguyên từ `cost/simulate-1-summary.md`)*

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| gv_chi_doc_the | 24 | 1 | 1589 | 504 | 1.0 | 3.1 |
| gv_hoi_tiep | 19 | 3 | 3144 | 967 | 2.1 | 7.1 |
| phu_trach_nhieu_lop | 7 | 2 | 1640 | 450 | 1.3 | 4.0 |

Tỉ lệ đạt dùng để tính: 15/24 (62%) — lượt run-2@20261128-101829 (`--rate-from eval/run-2.csv`)

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (3 người) | Chi phí / tháng — cơ sở (5 người) | Chi phí / tháng — cao (10 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **gpt-5.4-nano** (vào 0.2 · ra 1.25 $/1M) — **model chính** | $0.0013 | **$0.0020** | $0.0011 | $0.0822 | **$0.1370** | $0.2740 | **$0.0274** |
| gpt-5.4-mini (vào 0.75 · ra 4.5 $/1M) | $0.0047 | $0.0075 | $0.0039 | $0.3002 | $0.5003 | $1.00 | $0.1001 |
| gpt-5.4 (vào 2.5 · ra 15.0 $/1M) | $0.0156 | $0.0249 | $0.0131 | $1.00 | $1.67 | $3.34 | $0.3336 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**. Chi phí / câu hỏi đạt = chi phí / phiên ÷ 1,9 lượt hỏi TB / phiên ÷ tỉ lệ đạt. Token đo trên `gpt-5.4-nano`; `gpt-5.4-mini` và `gpt-5.4` tính giá trên cùng số token đó (bộ tách token khác thì số thật có thể lệch).

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): 1.500 phút ≈ 25 giờ / tháng cho 4 giảng viên → **≈ 375 phút ≈ 6,25 giờ / giảng viên / tháng** (15 buổi × 25 phút tiết kiệm — 25 phút *(tự ước tính)*). Người phụ trách học thuật không được tính vào impact §2 nhưng **có** tính vào chi phí → so sánh thiên về phía thận trọng.
- Chi phí / người / tháng (cơ sở, model `gpt-5.4-nano`): **$0.0274** (cả 5 người: $0.1370 / tháng). Chi phí / task thành công: **$0.0020** (đã chia cho tỉ lệ đạt lượt 2 = 62%).
- **Kết luận một dòng — đáng làm không:** **Đáng làm về chi phí** — ≈ $0,03 / người / tháng (kể cả `gpt-5.4` mạnh nhất cũng chỉ $0,33) để đổi lấy ≈ 6,25 giờ giảng viên / người / tháng; chi phí model không phải điểm nghẽn, **điểm nghẽn là chất lượng**: lượt 2 chỉ đạt 15/24 (nhóm `thuong` 0/8) nên phải sửa bộ lọc `_loc_synthetic` trước khi đưa vào dùng thật.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- **Độ nhạy theo model** (tỉ số từ bảng §2): `gpt-5.4-mini` ≈ 3,6× nano ($0.0047 / $0.0013 mỗi phiên), `gpt-5.4` ≈ 12× nano ($0.0156 / $0.0013). Kịch bản đắt nhất (`gpt-5.4`, 10 người) vẫn chỉ $3.34 / tháng. Trang model OpenAI ghi `gpt-5.4-nano` là **Deprecated** (xem 28/11/2026) → nếu phải đổi sang `gpt-5.4-mini`, cơ sở là $0.5003 / tháng ($0.1001 / người) — vẫn rất nhỏ so với impact.
- **Độ nhạy theo tỉ lệ đạt:** chi phí / task tỉ lệ nghịch với tỉ lệ đạt. Nếu sửa lỗi lượt 2 và đạt lại mức lượt 1 (20/24 = 83%) thì chi phí / task còn ≈ 0,75 lần hiện tại (62,5% ÷ 83,3%) — cần chạy lại lượt eval và mô phỏng mới mới là số chính thức.
- **Persona tốn nhất:** `gv_hoi_tiep` (3 lượt / phiên, 3144 token vào · 967 ra / phiên ≈ 2× persona khác). Cắt ngữ cảnh gửi model ở lượt hỏi tiếp là cần gạt hiệu quả nhất nếu sau này cần giảm.
- **Chi phí ngoài model:** giờ giảng viên duyệt thẻ (~5 phút / buổi *(tự ước tính)*) đã được trừ sẵn trong 25 phút tiết kiệm ở `spec.md` §2. Hosting / lưu trữ: bản demo chạy Streamlit cục bộ, data đã tổng hợp sẵn — chưa có số chi phí máy chủ khi dùng thật (chưa ước tính).
- **Quy mô:** chi phí tăng tuyến tính theo số người dùng (3 → 5 → 10 người: $0.08 → $0.14 → $0.27 / tháng với nano); ở quy mô khoá học, quyết định đáng làm hay không phụ thuộc chất lượng thẻ và thời gian giảng viên tiết kiệm được thật (cần người dùng xác nhận 25 phút), không phụ thuộc tiền model.
