# Data card — dữ liệu bản chạy thử dùng (bản đầu CP2)

> Không commit nguyên file data BTC — repo chỉ có số đã tổng hợp (không còn mã học viên).

## Dataset 1 · `review_stats.csv` — số tổng hợp bài ôn cuối ngày theo câu

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `lay_tin_hieu_ngay`, `lay_tin_hieu_cau` · đáp án mong đợi của câu thử · bằng chứng |
| Từ đâu | data BTC cấp: `data/preclass/answers.csv` + `events.csv` (khoá `chosen`) trong repo đề |
| Xử lý những bước gì | lọc `nguon = pre_post_post`, `lan_thu = 1`, `was_correct` True/False · nối `events.ref_id = answers.id` lấy đáp án đã chọn · gộp theo `ref` · bỏ mã học viên (script: `evidence/count_review.py`) |
| Số dòng | 156 câu ôn (1.968 lượt trả lời lần đầu, 77 học viên) · 83 câu có ≥ 10 lượt |
| Phiên bản / ngày lấy | data 05/11–25/11/2026, Day01–Day13 · tổng hợp 27/11/2026 |
| Nhãn | thật (đã tổng hợp) |
| Giới hạn | toàn khoá, chưa tách theo lớp · ngày sau rất ít người làm (Day09–13: 1–4 lượt / câu) · không có đề câu hỏi · không cho biết vì sao sai |

## Dataset 2 · `struggle_by_module.csv` — tín hiệu nghẽn theo phần bài

| | |
|---|---|
| Dùng để làm gì | nguồn cho `lay_tin_hieu_ngay` (mục "phần bài có tín hiệu nghẽn") |
| Từ đâu | data BTC cấp: `answers.csv` (thực hành), `events.csv` (`lab_completed`, `slide_text_asked`, `video_opened`), `chat.csv` (`video_question`) |
| Xử lý những bước gì | gộp theo `module_code`; lab trống `kc_code` (208/453 dòng) ghép bằng `lesson_id` + `lab_key`; video → module lấy theo cặp video/kc_code hay gặp nhất trong events; số học viên mở video làm mẫu số cho câu hỏi trợ giảng (script: `evidence/count_struggle.py`) |
| Số dòng | 99 module / lab |
| Phiên bản / ngày lấy | như Dataset 1 |
| Nhãn | thật (đã tổng hợp) |
| Giới hạn | không có nội dung câu hỏi chat (chỉ độ dài) · câu hỏi giữa video gần như không chấm (7 lượt) nên không dùng · lượt tua video không tách được tay / tự động nên không dùng |

## Dataset 3 · `question_bank.csv` — đề, đáp án, đoạn bài của câu ôn

| | |
|---|---|
| Dùng để làm gì | `lay_de_cau_hoi` → AI phân biệt hiểu sai chung / câu hỏi gây nhầm, soạn quiz nháp |
| Từ đâu | nhóm chép / viết lại từ pre-class (đăng nhập tài khoản học viên của nhóm) |
| Xử lý | mỗi dòng gắn đúng `ref`, `lesson_id`, `kc_code` như Dataset 1 |
| Số dòng | **0 — đang chép** (ưu tiên các câu bị gắn cờ) |
| Nhãn | tài liệu khoá (trích ngắn / viết lại) |

## Dataset 4 · data lớp tự dựng (đang làm)

Bảng lượt trả lời dựng theo **đúng khung `answers.csv`** (cùng cột, `lesson_id`, `kc_code`, `ref` thật), dùng cho câu thử về một lớp cụ thể. Nhãn **`synthetic`**. Khi xong ghi: cách dựng, seed, người kiểm, số dòng kiểm tay. **Không dùng làm bằng chứng pain.**
