# Đào data — cách đếm và kết quả

## 1. Cách đếm — viết TRƯỚC khi chạy

- Data dùng: `data/preclass` của repo đề (05/11–25/11/2026, Day01–Day13): `answers.csv`, `events.csv`, `chat.csv`.
- Đếm gì: các chỗ học viên **sai / khó hiểu / nghẽn**, theo câu ôn và theo phần bài (module):
  1. Bài ôn cuối ngày: `nguon = pre_post_post`, `lan_thu = 1` → lượt sai / lượt trả lời; đáp án sai được chọn nhiều nhất (`chosen` trong `events.data`).
  2. Thực hành: `nguon = thuc_hanh`, `lan_thu = 1` → lượt sai; `lab_completed` có `skipped = true` → lượt bỏ qua / lượt kết thúc lab.
  3. Câu hỏi trợ giảng dưới video (`chat.csv`, `channel = video_question`) / số học viên đã mở video đó.
  4. Bôi đen chữ trên slide để hỏi (`slide_text_asked`), theo module và số slide.
- **Mẫu số:** tỉ lệ sai một câu = lượt sai lần đầu / lượt trả lời lần đầu của **câu đó**; câu hỏi trợ giảng chia cho **số học viên mở video**, không chia cho 436 hay 721.
- Ngưỡng mẫu: câu có dưới 10 lượt lần đầu → "chưa đủ dữ liệu".
- Script: `evidence/count_review.py` (theo câu) · `evidence/count_struggle.py` (theo module). Chạy: `python -I evidence/count_struggle.py <đường dẫn data/preclass>`.

## 2. Đọc trước, đếm sau

Đã đọc dòng đầu các file, `column_dictionary.csv`, `event_types.csv`. Kiểu hành vi thấy được:
- Học viên làm bài ôn một lần rồi thôi: **0/399** lượt sai lần đầu có làm lại cùng câu.
- Lượt sai nhiều câu **dồn vào cùng một đáp án** → có thể hiểu sai chung, hoặc câu hỏi / đáp án gây nhầm.
- Nhiều học viên **bấm bỏ qua** bài thực hành.
- Câu hỏi trợ giảng và lượt bôi đen slide **tập trung** vào vài module / vài slide.
- Không dùng: câu hỏi giữa video (chỉ 7 lượt có chấm) · tua video (`by = player` gần hết, không tách được tay hay tự động).

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Bài ôn: lượt trả lời lần đầu sai | 399 / 1.968 | 20,3% | 77 học viên, 156 câu |
| Lượt sai lần đầu có làm lại | 0 / 399 | 0% | sai là bỏ đó |
| Câu ôn đủ mẫu (≥10 lượt) có tỉ lệ sai ≥30% | 20 / 83 | 24% | |
| Câu ôn đủ mẫu có ≥50% lượt sai dồn vào 1 đáp án (≥5 lượt sai) | 18 / 83 | 22% | dấu hiệu hiểu sai chung / câu gây nhầm |
| Câu ôn chưa đủ mẫu | 73 / 156 | 47% | Day06–13 ít người làm |
| Lab bấm bỏ qua | 102 / 453 | 22,5% | |
| Bước thực hành sai lần đầu | 23 / 503 | 4,6% | thực hành ít sai, nhưng bị bỏ qua |
| Câu hỏi trợ giảng gắn được module | 1.107 / 1.108 | | |
| Lượt bôi đen slide để hỏi | 433 | | |

## 4. ≥5 ví dụ cụ thể (mã câu / module, không có mã học viên)

1. `d05-on-cot-canvas` (KC `ai_product_canvas`): sai 12/15 lần đầu, **12/12 lượt sai cùng chọn A** → cần xem lại đề / đáp án trước khi kết luận học viên hiểu sai.
2. `d01-on-chatbot-la-ung-dung`: sai 16/41 (39%), 9/16 lượt sai chọn C.
3. `d03-on-tong-5-diem`: sai 12/20 (60%).
4. `lab-d02-lab-hoi-dong-gate`: bị bỏ qua 10/17 lượt (59%).
5. `program-day01:ai-llm-foundation:module-2`: 115 câu hỏi trợ giảng / 187 học viên mở video; slide 18 bị bôi đen để hỏi 27 lượt.
6. `program-day01:ai-llm-foundation:module-1`: slide 9 bị bôi đen để hỏi 24/28 lượt của cả module.

## 5. Giới hạn của data

Data cho biết học viên **sai / hỏi / bỏ ở đâu**, không cho biết **vì sao**; không có nội dung câu hỏi chat; số là toàn khoá, chưa tách theo lớp; ngày sau ít người làm.
→ Kiểm lại bằng phỏng vấn giảng viên / lab coach (hiện họ biết lớp vướng gì bằng cách nào) và học viên (vì sao chọn đáp án sai ở các câu trên) — ghi ở `evidence/interviews/`.
