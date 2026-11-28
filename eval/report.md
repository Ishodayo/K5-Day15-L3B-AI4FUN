# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-081440` | 20/24 | 83% | 5/8 (62%) | 10/11 (91%) | 5/5 (100%) | **Đạt** chuẩn CP2 *(83% ≥ 80%, 100% `tu_choi`, 0 lỗi số/mã lạ; riêng metric `goi_y_dung_duoc` ở nhóm `thuong` đạt 5/8 = 62,5% < 80%)* |
| 2 | `run-2@20261128-101829` | 15/24 | 62% | 0/8 (0%) | 10/11 (91%) | 5/5 (100%) | **Chưa đạt** *(62% < 80%; đạt 100% `tu_choi` và 0 lỗi số/mã lạ, nhưng `thuong` rớt 0/8 do bộ lọc `_loc_synthetic` bỏ toàn bộ phần D)* |

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

- Nhắm vào nhóm lỗi: **Xử lý đề `synthetic` và chất lượng gợi ý trên 4 câu trượt lượt 1 (`B02, B05, B17, B18`)** — vì sao là nhóm **đau nhất với người dùng**: giảng viên cần thấy cảnh báo khả năng đề gây nhầm khi lớp sai dồn 1 đáp án (`B05`), cần gợi ý điều chỉnh bài giảng không bị sai nghĩa do đoán từ mã không dấu (`B02`) và không bị lọt mã kỹ thuật `KC ...` (`B17, B18`).
- Đã sửa gì (trong `codebase/agent.py`, commit trước lượt 2):
  1. Gắn cảnh báo `"Có khả năng câu hỏi gây nhầm; giảng viên cần xem đề gốc trước khi kết luận"` trực tiếp ở tầng code (`_the_cau`) khi tỷ lệ sai dồn 1 đáp án `≥ 50%`.
  2. Ẩn mã `KC ...` khỏi thẻ số liệu và thêm luật chặn mã `KC` thô trong `_kiem_dau_ra_ai`.
  3. Đưa đề `synthetic` vào prompt dưới nhãn `"câu hỏi ví dụ"` (tách khỏi số liệu thật) để AI soạn gợi ý/quiz ôn nháp cụ thể hơn, đồng thời thêm hàm `_loc_synthetic` để fail-closed nếu AI suy đoán về học viên hoặc viết sai định dạng `[mã thẻ]`.
- Kết quả: nhóm lỗi đó **0/4 → 1/4** (`B05` chuyển từ trượt sang đạt; `B02, B17, B18` vẫn trượt) · tổng **83% → 62%** (20/24 → 15/24).
- Câu nào **tệ đi** sau khi sửa: **6 câu chuyển từ đạt → trượt**:
  - `B01, B03, B04, B15, B16` (`thuong`): bộ lọc `_loc_synthetic` dùng regex bắt buộc `[mã_thẻ]` có ngoặc vuông (`^\[ref\]`), nhưng `gpt-5.4-nano` xuất `ref Loại: ...` không có ngoặc vuông → toàn bộ 10/10 câu có đề synthetic bị bỏ sạch phần D (`Đã bỏ phần diễn giải của AI vì không nhận diện được phần gợi ý ví dụ`), khiến 8/8 câu `thuong` mất nhãn phân loại và gợi ý điều chỉnh bài giảng.
  - `B20` (`kho`): câu chưa có đề nhưng AI vẫn tự bịa quiz ôn nháp dựa trên việc đoán sai mã không dấu `nguoi-duyet-cho-co` thành `"ai có quyền duyệt/đồng ý"`, và in nguyên chuỗi `Loại: cần xem thêm | câu hỏi gây nhầm`.

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào:
  1. **Bộ lọc `_loc_synthetic` bắt định dạng quá cứng (nghiêm trọng — làm hỏng 10/10 câu có đề synthetic):** chỉ vì model bỏ dấu ngoặc vuông quanh `ref` mà toàn bộ phần gợi ý AI bị xoá, làm giảng viên chỉ nhận được bảng số liệu thô, mất giá trị cốt lõi của Class Pulse.
  2. **AI vẫn bịa quiz khi chưa có đề và đoán sai mã không dấu (`B10, B20`):** giảng viên có thể nhận câu quiz ôn nháp sai hẳn nội dung bài học (vd đoán `cho-co` → `"đồng ý"`, `ba-ban` → `"bàn chính sách"`).
  3. **Bug điều kiện ở `_the_cau` (`B09`):** kiểm tra `don / co_da >= 0.5` nhưng thiếu điều kiện `co_da >= 5`, nên câu sai rất thấp (`2/35`, `1/2` chọn B) vẫn in cảnh báo `"Có khả năng câu hỏi gây nhầm"` mâu thuẫn với kết luận `"không cần ôn"`.
- Nếu có thêm 1 tuần:
  1. Nới regex của `_loc_synthetic` (chấp nhận cả `[ref]` lẫn `ref` đầu dòng hoặc ép model trả JSON/structured output) và bổ sung điều kiện `co_da >= 5` trong `_the_cau`.
  2. Xin bộ đề gốc pre-class từ BTC để thay thế 19 dòng `synthetic` trong `data/question_bank.csv`, giúp AI phân tích đúng nguyên nhân sai thay vì luôn phải trả `"cần xem thêm"`.
  3. Chặn bằng code không cho xuất quiz ôn nháp ở các câu/module chưa có đề (`B10, B20`), đồng thời mở rộng tách số liệu theo từng lớp (L3A/L3B) và thử nghiệm với 2–3 giảng viên thật (`validation/log.md`).
