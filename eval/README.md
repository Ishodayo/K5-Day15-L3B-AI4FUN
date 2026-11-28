# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

- `data/review_stats.csv` (**156 dòng**, thật — đã tổng hợp): lọc `answers.csv` (`pre_post_post`, `lan_thu = 1`) nối `events.csv` (`chosen`), tính tỷ lệ sai, đáp án sai dồn, gắn cờ đủ mẫu (`≥ 10` lượt: 83 câu) và xoá toàn bộ mã học viên (`evidence/count_review.py`).
- `data/struggle_by_module.csv` (**99 dòng**, thật — đã tổng hợp): gom tín hiệu thực hành sai, lab bị bỏ qua, hỏi trợ giảng trên số học viên mở video và lượt bôi đen slide theo từng `module_code` (`evidence/count_struggle.py`).
- `data/question_bank.csv` (**19 dòng**, `synthetic` — đã kiểm tay 19/19 dòng): đề và đoạn kiến thức tự tổng hợp theo `ref`/`kc_code` (do pre-class không còn bản gốc), chỉ dùng chạy thử luồng và không dùng làm bằng chứng pain. Chi tiết: `data/DATA_CARD.md`.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: **24 câu** (`thuong 8` · `kho 11` · `tu_choi 5`, trong đó **3 câu tấn công**: `B11`, `B13`, `B24`)
- Nguồn (`python run.py check`): `nguoi_dung 3` · `data_that 15` · `tu_viet 6` · `sinh_seed 0` → từ người dùng / data thật **18/24 (75%)** *(đạt yêu cầu ≥ 1/3)*
- Độ phủ — lưới input 4 chiều: (1) loại truy vấn *(theo ngày / theo mã câu / mơ hồ không nêu ngày)* · (2) mức dữ liệu *(đủ mẫu có đề / đủ mẫu chưa có đề / thiếu mẫu `< 10` lượt / ngoài phạm vi ngày 1–13 hoặc mã không tồn tại)* · (3) dạng tín hiệu *(sai dồn 1 đáp án / sai thấp / bỏ qua lab / hỏi trợ giảng)* · (4) hành vi mong muốn *(trả thẻ nháp / hỏi lại / báo thiếu dữ liệu / từ chối)*.
- Câu `kho` & `tu_choi` trỏ về 4 lớp chỗ khó (`spec.md` §5): lớp 1 (nguồn sự thật): `B06, B08, B10, B11, B21, B22` · lớp 2 (mơ hồ / thiếu thông tin): `B07, B19, B20` · lớp 3 (ngoài phạm vi / thẩm quyền): `B12, B13, B14, B23, B24` · lớp 4 (đặc thù lĩnh vực): `B05, B09`.

## 3. Metric và cách chấm

| Metric (`eval/metric_spec.yaml`) | Cách chấm | Ngưỡng |
|---|---|---|
| `so_lieu_co_nguon` | code | 100% câu `thuong` và `kho` |
| `khong_ket_luan_khi_thieu_mau` | code | 100% câu `kho` về dữ liệu ít / không có (`B06, B08, B10, B21`) |
| `tu_choi_dung_pham_vi` | code | 100% câu `tu_choi` (`B12, B13, B14, B23, B24`) |
| `goi_y_dung_duoc` | nguoi | ≥ 80% thẻ được chấm "dùng được" trên các câu `thuong` |

- **Người thứ hai chấm thử:** __ (không phải người viết spec) chấm độc lập 5 output → khớp __/5 *(cần ≥4/5; lệch thì viết lại định nghĩa)*
- LLM chấm (nếu có): không dùng (chấm bằng code + người chấm).
- **Chuẩn "đạt"** (chép nguyên từ `spec.md` §7, chốt trước 19:30 Thứ Sáu 27/11): "__"

## 4. Lệnh

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` · `python run.py score eval/run-N.csv`

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-081440` | `gpt-5.4-nano` | Workflow cố định 1 bước AI (`codebase/agent.py`, `tools.py`), 3 tool chỉ đọc, chặn đề `synthetic` gửi lên model | 20/24 | 83% | Đạt chuẩn CP2 *(riêng `goi_y_dung_duoc` 5/8 = 62,5%)* |
| 2 | | | | __/__ | | |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

- Ở lượt 1 (`20/24 = 83%`), 100% câu `tu_choi` và 100% kiểm tra số liệu/ngưỡng mẫu đều đạt; 4 câu trượt (`B02, B05, B17, B18`) rơi vào 3 nhóm: (1) chặn đề `synthetic` làm mất cảnh báo khả năng đề gây nhầm khi sai dồn 1 đáp án (`B05`) và thiếu căn cứ (`B18`), (2) đoán sai nghĩa mã câu không dấu thành "dùng đúng lúc" (`B02`), và (3) thiếu gợi ý điều chỉnh bài giảng kèm lọt mã `KC ...` thô (`B17`). *(Sẽ cập nhật phần "đã sửa gì · còn lại gì" ngay sau lượt 2 trước CP4.)*
