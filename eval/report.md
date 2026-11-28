# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-081440` | 20/24 | 83% | 5/8 (62%) | 10/11 (91%) | 5/5 (100%) | **Đạt** chuẩn CP2 *(83% ≥ 80%, 100% `tu_choi`, 0 lỗi số/mã lạ; riêng metric `goi_y_dung_duoc` ở nhóm `thuong` đạt 5/8 = 62,5% < 80%)* |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Chặn đề `synthetic` quá cứng khiến không nêu khả năng đề/đáp án gây nhầm hoặc thiếu căn cứ | 2 | B05, B18 |
| Đoán sai nghĩa kiến thức từ mã câu không dấu khi thiếu đề | 1 | B02 *(kèm lỗi nhẹ đọc nhầm "ba bản" → "ba ban" ở B10)* |
| Thiếu gợi ý điều chỉnh bài giảng và lọt mã kỹ thuật thô (`KC ...`) vào câu trả lời | 1 | B17 *(kèm biểu hiện phụ in mã KC thô ở B04, B18)* |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| **B05** (`kho`) | `Ngày 5 lớp đang vướng gì?` | `d05-on-cot-canvas Loại: cần xem thêm / Vì sao: chưa có đề câu hỏi — giảng viên xem đề trước khi kết luận. / Gợi ý: Điều chỉnh phần trình bày theo đúng ngữ cảnh đề gốc và chèn 1 quiz ôn nháp bám sát câu đã hỏi.` | Dù đã nêu đúng `12/15` và `12/12` chọn A, phần diễn giải **không nêu khả năng đề/đáp án gây nhầm** (trượt `pass_criterion`) vì code tự ẩn toàn bộ đề có nhãn `synthetic` và prompt cấm nhận định đề gây nhầm ngay cả khi 100% lượt sai dồn vào 1 đáp án. |
| **B02** (`thuong`) | `Ngày 3 lớp hiểu sai gì nhiều nhất?` | `d03-on-dung-dung-luc Loại: cần xem thêm / ... / Gợi ý: chốt lại tiêu chí khi nào “dùng đúng lúc” trong quy trình agent (tránh nhầm điều kiện)...` | Khi thiếu đề, AI tự dịch ngược mã không dấu `d03-on-dung-dung-luc` (KC `trace_based_agent_evaluation` = **dừng đúng lúc**) thành **"dùng đúng lúc"**, làm lệch hoàn toàn khái niệm kiến thức (trượt metric `goi_y_dung_duoc`). |
| **B17** (`thuong`) | `Xem chi tiết câu d01-on-chon-tang-model giúp tôi` | `d01-on-chon-tang-model Loại: cần xem thêm / Vì sao: chưa có đề câu hỏi — giảng viên xem đề trước khi kết luận. / Gợi ý: Ôn nháp bằng câu hỏi trắc nghiệm dạng “khi nào chọn KC model_tier_selection ở tầng nào”...` | **Thiếu gợi ý điều chỉnh bài giảng** cho giảng viên; lại đề xuất câu quiz ôn nháp chứa nguyên mã kỹ thuật thô `KC model_tier_selection` dù thẻ đang ghi chưa có đề (trượt metric `goi_y_dung_duoc`). |
| **B18** (`thuong`) | `Câu d02-on-can-agent học viên sai nhiều là do hiểu sai kiến thức hay do đề gây nhầm? Cho tôi xem căn cứ để tự đánh giá` | `d02-on-can-agent Loại: cần xem thêm / Vì sao: chưa có đề câu hỏi — giảng viên xem đề trước khi kết luận. / Gợi ý: rà soát lại phần “KC select_rule_workflow_agent_level” trong bài...` | Không trích được căn cứ tham chiếu từ `question_bank.csv` (do code chặn đề `synthetic`) và lặp nguyên mã thô `KC select_rule_workflow_agent_level` thay vì diễn giải dễ đọc cho giảng viên (trượt `pass_criterion`). |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
