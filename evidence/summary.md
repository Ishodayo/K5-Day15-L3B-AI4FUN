# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ **Đạt** — có x/N và %, cách đếm viết trước khi chạy, 2 script chạy lại được (`evidence/count_review.py`, `evidence/count_struggle.py`), 6 ví dụ theo mã câu / phần bài | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ Chưa đạt — 1 người (P1), dùng để kiểm lại data | `evidence/interviews/P1.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ Không làm | — |

## 2. Số chính

- **Đào data** (data pre-class BTC cấp, 05/11–25/11/2026, Day01–Day13; số đối chiếu lại với `data/review_stats.csv`, `data/struggle_by_module.csv`):
  - Bài ôn cuối ngày: **399/1.968 lượt trả lời lần đầu sai (20,3%)** — 77 học viên, 156 câu.
  - Lượt sai lần đầu có làm lại cùng câu: **0/399 (0%)** — sai là bỏ đó, không ai sửa.
  - Câu ôn đủ mẫu (≥10 lượt) có **≥50% lượt sai dồn vào cùng 1 đáp án**: **18/83 (22%)** — dấu hiệu cả lớp hiểu sai cùng một kiểu, hoặc câu / đáp án gây nhầm.
  - Câu ôn đủ mẫu có tỉ lệ sai ≥30%: **20/83 (24%)**.
  - Lab bị bấm bỏ qua: **102/453 (22,5%)**; bước thực hành sai lần đầu chỉ 23/503 (4,6%) → thực hành ít sai nhưng hay bị bỏ.
  - 1.107 câu hỏi trợ giảng gắn được module, dồn vào vài phần bài (vd day01 module-2: 115 câu / 187 học viên mở video).
  - Câu ôn chưa đủ mẫu: 73/156 (47%) — Day06–13 ít người làm, nên công cụ phải nói "chưa đủ dữ liệu".
- **Phỏng vấn:** 1/3 người *(chưa đạt ngưỡng; n nhỏ không ghi %)* — P1 gặp pain **một phần** · số lần / tháng: P1 không hỏi được · mỗi lần mất: không hỏi được.
- **Khảo sát:** không làm.

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Giảng viên, phụ trách học thuật *(TV2 xác nhận vai 28/11/2026)* | Một phần — đồng ý giảng viên *muốn* biết lớp sai dồn vào đâu, nhưng chưa kể một lần cụ thể | không hỏi | không hỏi | không nêu cách hiện tại |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "Bản thân cái nội dung này nó có thể bị sai… thì nó sẽ là một kiểu nhé. Còn cái kiểu thứ hai, đấy là bọn em làm câu trả lời bị sai." — **P1** (giảng viên nhìn các bạn sai dồn vào đâu để hôm sau xoáy vào phần đó)
2. "Nội dung bài giảng phải được validate chuẩn để mới được đưa lên… cả quiz nó cũng phải chuẩn rồi, vì lúc đấy bọn em làm đúng hay làm sai thì cái insight đấy là về việc hiểu nó sẽ chính xác." — **P1**
3. `d05-on-cot-canvas` (KC `ai_product_canvas`): sai **12/15** lần đầu, **12/12 lượt sai cùng chọn A** — dòng `d05-on-cot-canvas` trong `data/review_stats.csv`. Cả lớp sai một kiểu, hoặc đáp án / đề gây nhầm → giảng viên cần xem đề trước khi giảng lại.
4. `d01-on-chatbot-la-ung-dung`: sai **16/41 (39%)**, **9/16** lượt sai chọn cùng đáp án C — dòng `d01-on-chatbot-la-ung-dung` trong `data/review_stats.csv`.
5. `d03-on-tong-5-diem`: sai **12/20 (60%)** lần đầu — dòng `d03-on-tong-5-diem` trong `data/review_stats.csv`.
6. `lab-d02-lab-hoi-dong-gate`: bị bấm bỏ qua **10/17 lượt (59%)** — dòng `program-day02:ai-problem-definition:lab-d02-lab-hoi-dong-gate` trong `data/struggle_by_module.csv`.
7. `program-day01:ai-llm-foundation:module-2`: **115 câu hỏi trợ giảng / 187 học viên mở video**; slide 18 bị bôi đen để hỏi 27 lượt — dòng cùng mã trong `data/struggle_by_module.csv`.

## 4. Các nguồn có khớp nhau không

Data nói: học viên **sai dồn vào cùng một chỗ** (18/83 câu đủ mẫu dồn ≥50% vào 1 đáp án; câu hỏi trợ giảng dồn vào vài phần bài) và **sai rồi không ai sửa** (0/399 lượt sai có làm lại). Người dùng nói (P1): giảng viên muốn nhìn được các bạn sai dồn vào khu vực nào để hôm sau xoáy vào phần đó.

- **Khớp:** tín hiệu "sai dồn theo câu / phần bài" trong data đúng là thứ P1 nói giảng viên cần nhìn → lát cắt gom theo câu / phần bài là hợp lý.
- **Lệch 1:** P1 cho rằng quiz đã được validate trước khi lên, nên sai = học viên chưa hiểu. Data có câu như `d05-on-cot-canvas` (12/12 lượt sai cùng chọn A) — có thể là đề / đáp án gây nhầm. Vì vậy thẻ không kết luận thay: nêu cả hai khả năng và để giảng viên xem đề (lỗi nội dung đi luồng kiểm duyệt riêng qua giảng viên, theo P1).
- **Lệch 2:** data cho biết **sai ở đâu**, P1 chưa cho biết **hiện giảng viên biết bằng cách nào và mất bao lâu** (buổi nói chuyện không đi vào một lần cụ thể). Chưa có số phút từ người dùng → impact ở `spec.md` §2 ghi phần thời gian là *(tự ước tính)*.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md` (chép từ canvas CP1, commit `120e334`, viết trước khi có script đếm): **phải đổi**.
- **Đúng:** có những ý nhiều học viên sai cùng một kiểu (18/83 câu; `d05-on-cot-canvas` 12/12 cùng một đáp án) và lỗi không được sửa (0/399 làm lại).
- **Phải đổi:** người dùng chính là **giảng viên** (người điều chỉnh bài giảng buổi sau), không phải lab coach/TA — theo P1; tín hiệu không chỉ là bài ôn mà cả lab bỏ qua (102/453) và câu hỏi trợ giảng (1.107 câu).
- **Chưa kiểm được:** vế "người phụ trách buổi học không có cách nhanh để biết lớp hiểu sai ý nào" — P1 không kể cách hiện tại.

Điều vẫn chưa biết: giảng viên hiện có tự gom các tín hiệu này không, mất bao lâu mỗi buổi · vì sao học viên chọn đáp án sai (vd `d05-on-cot-canvas` sai do đề hay do hiểu) · số liệu tách theo từng lớp (data là toàn khoá).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| P1 · giảng viên, phụ trách học thuật | 27/11/2026 ~18:35, trực tiếp, có ghi âm | ☑ |
