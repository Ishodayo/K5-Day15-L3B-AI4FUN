# Data Card — Dữ liệu bản chạy thử Class Pulse (Nhóm AI4FUN · Track A)

> **Cam kết dữ liệu & ẩn danh:** Repo công khai **không** chứa nguyên file CSV BTC cấp, **không** chứa mã học viên (`hv`) hay thông tin cá nhân, và **không** commit nguyên tài liệu khoá học. Mọi dữ liệu trong `data/` đều là số liệu đã tổng hợp, đoạn trích ngắn/viết lại hoặc dữ liệu `synthetic` có gắn nhãn rõ ràng.

---
## Tổng quan các dataset trong `data/`

| # | File | Cách tạo ra | Nội dung chứa | Ứng dụng | Nhãn dữ liệu | Quy mô hiện tại | Trạng thái |
|---|---|---|---|---|---|---|---|
| 1 | `data/review_stats.csv` | Chạy tự động `evidence/count_review.py` từ answers.csv + events.csv | Lượt làm lần đầu, tỷ lệ sai, đáp án sai chọn nhiều nhất và cờ (flags) đủ mẫu (`≥ 10` lượt) theo từng câu ôn | Xác định câu ôn bị nghẽn, lọc câu thiếu mẫu và cấp số liệu chuẩn cho thẻ | **Thật** | **156 dòng** (156 câu ôn; 83 câu đủ mẫu ≥ 10 lượt) | Sẵn sàng |
| 2 | `data/struggle_by_module.csv` | Chạy tự động `evidence/count_struggle.py` từ answers.csv, events.csv, chat.csv | Tỷ lệ sai thực hành, tỷ lệ bỏ qua lab, số câu hỏi trợ giảng và slide bị highlight hỏi nhiều nhất theo từng module/lab | Bắt các điểm nghẽn giảng dạy và thực hành ngoài bài ôn cuối ngày | **Thật** | **99 dòng** (module & mini lab) | Sẵn sàng |
| 3 | `data/question_bank.csv` | Trích ngắn / viết lại từ pre-class | Đề bài, các đáp án, đáp án đúng và đoạn bài giảng ngắn gắn đúng mã câu (`ref`) | Cấp căn cứ ngữ cảnh để AI đề xuất hướng giảng bài đúng trọng tâm và tạo quiz để học phần kiến thức đó | **Tài liệu khoá** *(trích ngắn / viết lại)* | **0 dòng** *(mới có header 8 cột)* | Đang nạp trước CP3 |


---

## Dataset 1 · `data/review_stats.csv` — Thống kê bài ôn cuối ngày theo từng câu

| Hạng mục | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn dữ liệu chính cho công cụ `lay_tin_hieu_ngay` và `lay_tin_hieu_cau`; đối chiếu đáp án `expected` trong `eval/benchmark.csv`; số liệu bằng chứng pain. |
| **Nguồn gốc** | Bộ `data/preclass/` do BTC cấp trong repo đề: `answers.csv` kết hợp `events.csv` (trường JSON `chosen` của sự kiện `answer_submitted`). |
| **Quy trình xử lý & tái lập** | 1. **Lọc:** `nguon = pre_post_post`, `lan_thu = 1`, chỉ giữ `was_correct ∈ {True, False}` (ô trống ≠ sai).<br>2. **Ghép nối:** Nối 1-1 `events.ref_id = answers.id` (khớp 1.968/1.968 lượt) để lấy đáp án học viên chọn (`A/B/C/D`).<br>3. **Tổng hợp & ẩn danh:** Gộp theo `(ref, lesson_id, kc_code)`, đếm tỷ lệ sai, phân bố đáp án sai, tỷ lệ làm lại (`lan_thu ≥ 2`), gắn cờ ngưỡng mẫu `du_mau` (`n_lan_dau ≥ 10`) và **xóa toàn bộ cột `hv`**.<br>• **Script tái lập:** `python -I evidence/count_review.py <đường-dẫn-data/preclass>` |
| **Cấu trúc cột (12 cột)** | `ref`, `lesson_id`, `kc_code`, `n_lan_dau`, `n_hoc_vien`, `sai_lan_dau`, `ti_le_sai`, `dap_an_sai_nhieu_nhat`, `so_chon_dap_an_do`, `sai_co_dap_an`, `sai_co_lam_lai`, `du_mau` |
| **Quy mô** | **156 dòng** (156 câu ôn), tổng hợp từ **1.968 lượt trả lời lần đầu** của **77 học viên** (399 lượt sai). Trong đó **83 câu** đạt ngưỡng (`≥ 10` lượt) và **73 câu** dưới ngưỡng (`< 10` lượt). |
| **Phiên bản / ngày lấy** | Nhật ký gốc: `05/11/2026 – 25/11/2026` (Day01–Day13) · Ngày tổng hợp: `27/11/2026`. |
| **Nhãn dữ liệu** | **Thật** *(đã tổng hợp, không còn định danh cá nhân)*. |
| **Giới hạn & thiên lệch** | • Số liệu gộp **toàn khoá**, chưa tách riêng từng lớp (L3A / L3B).<br>• Các ngày sau rất ít người làm bài ôn (Day09–Day13 chỉ có 1–4 lượt/câu) → bắt buộc gắn cờ "chưa đủ dữ liệu".<br>• Không chứa văn bản đề/đáp án và không tự chứng minh nguyên nhân vì sao học viên sai. |

---

## Dataset 2 · `data/struggle_by_module.csv` — Tín hiệu nghẽn theo từng phần bài (module / lab)

| Hạng mục | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn cho công cụ `lay_tin_hieu_ngay` để hiển thị mục "Phần bài có tín hiệu nghẽn" (lab bị bỏ qua, thực hành sai, hỏi trợ giảng nhiều, slide bị hightlight hỏi nhiều). |
| **Nguồn gốc** | Bộ `data/preclass/` do BTC cấp: `answers.csv` (`thuc_hanh`, `pre_post_post`), `events.csv` (`lab_completed`, `slide_text_asked`, `video_opened`), và `chat.csv` (`channel = video_question`). |
| **Quy trình xử lý & tái lập** | 1. **Gom nhóm:** Tổng hợp mọi tín hiệu theo `module_code` (định dạng `<lesson_id>:module-N` hoặc `<lesson_id>:lab-...`).<br>2. **Làm sạch & ánh xạ:** Với 208/453 dòng `lab_completed` bị trống `kc_code`, ghép bằng `lesson_id + lab_key`; ánh xạ `video → module` dựa trên cặp `(video, kc_code)` xuất hiện nhiều nhất trong `events.csv`.<br>3. **Chuẩn hóa mẫu số & ẩn danh:** Lấy số học viên đã mở video (`hv_mo_video`) làm mẫu số cho tỷ lệ hỏi trợ giảng (`hoi_ta_moi_hv`); xóa toàn bộ mã học viên `hv`.<br>• **Script tái lập:** `python -I evidence/count_struggle.py <đường-dẫn-data/preclass>` |
| **Cấu trúc cột (17 cột)** | `module_code`, `lesson_id`, `on_n`, `on_sai`, `on_ti_le_sai`, `th_n`, `th_sai`, `th_ti_le_sai`, `lab_n`, `lab_bo_qua`, `lab_ti_le_bo_qua`, `hv_mo_video`, `hoi_ta`, `hoi_ta_moi_hv`, `boi_slide`, `slide_hoi_nhieu_nhat`, `so_lan_slide_do` |
| **Quy mô** | **99 dòng** (gồm 69 module có dữ liệu mở video, 30 mục có dữ liệu lab, 25 mục có dữ liệu bước thực hành). |
| **Phiên bản / ngày lấy** | Nhật ký gốc: `05/11/2026 – 25/11/2026` (Day01–Day13) · Ngày tổng hợp: `27/11/2026`. |
| **Nhãn dữ liệu** | **Thật** *(đã tổng hợp, không còn định danh cá nhân)*. |
| **Giới hạn & tín hiệu đã loại bỏ** | • Không có nội dung chữ câu hỏi học viên gửi trợ giảng (chỉ có số lượt).<br>• **Đã chủ động loại bỏ:** câu hỏi giữa video (`video_quiz`, chỉ có 7 lượt chấm — quá ít) và lượt tua video (`video_seeked`, 4.282/4.322 lượt là `by = player`, không tách chắc chắn được tua tay với tự động nhảy). |

---

## Dataset 3 · `data/question_bank.csv` — Đề bài, đáp án & đoạn bài giảng tham chiếu

| Hạng mục | Chi tiết |
|---|---|
| **Dùng để làm gì** | Nguồn cho công cụ `lay_de_cau_hoi`, giúp AI có căn cứ phân biệt *hiểu sai chung* với *câu hỏi gây nhầm* và soạn câu quiz ôn nháp bám sát bài học. |
| **Nguồn gốc** | Nhóm trích ngắn / viết lại từ nền tảng pre-class của khoá (truy cập bằng tài khoản học viên của nhóm). **Không** sao chép nguyên văn toàn bộ tài liệu khoá học. |
| **Quy trình xử lý** | Gắn khớp khóa ngoại `ref`, `lesson_id`, `kc_code` đúng 1-1 với `review_stats.csv`; ưu tiên nạp các câu bị gắn cờ sai cao ở Day01–Day05. |
| **Cấu trúc cột (8 cột)** | `ref`, `lesson_id`, `kc_code`, `de`, `cac_dap_an`, `dap_an_dung`, `doan_bai`, `nguon` |
| **Quy mô** | **0 dòng** *(hiện mới tạo file header — đang nạp 8–10 câu ưu tiên trước CP3; sẽ cập nhật lại số dòng chính xác khi hoàn tất)*. |
| **Phiên bản / ngày lấy** | Trích lập ngày `27–28/11/2026` từ phiên bản bài giảng pre-class hiện hành. |
| **Nhãn dữ liệu** | **Tài liệu khoá** *(trích đoạn ngắn / viết lại có ghi rõ cột `nguon`)*. |
| **Giới hạn** | Chỉ phủ các câu ưu tiên dùng cho demo & bộ câu thử; với các câu chưa có trong file, hệ thống trả về `"chưa có đề"` và yêu cầu giảng viên tự kiểm đề trước khi kết luận. |

---