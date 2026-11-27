# Phân công CP3 · AI4FUN · Class Pulse

> **Nộp CP3: 10:00 Thứ Bảy 28/11.** Sáng Thứ Bảy không có lớp → phần tối nay xong **trước 23:00**.
> Đã chốt ở CP2, **không sửa**: chuẩn "đạt" (`spec.md` §7), `eval/metric_spec.yaml`, câu thử B01–B14, số bằng chứng. Thay đổi khác ghi 1 dòng vào `spec.md` §10.

**Nguyên tắc chia:** mỗi người **ôm trọn** một phần, từ đầu đến khi ra file nộp được. Không ai làm dở rồi chuyển cho người khác làm nốt.

## CP3 cần nộp → ai chịu trách nhiệm

| Yêu cầu CP3 | Người làm trọn |
|---|---|
| Bằng chứng pain: ≥1 nguồn đủ ngưỡng + ≥5 trích dẫn / ví dụ | **Trà** |
| Bảng impact | **Trà** |
| Bản chạy thử gọi AI thật · video 30 giây | **Duy** |
| 20–30 câu thử + `eval/run-1.csv` + kết quả `score` | **Hiếu** |
| `spec.md` §0–§7 · gộp PR · nộp | **Nam** |

## Cách làm chung

- Mỗi người một branch, mở PR vào `main` **trước 23:00**. Nam gộp.
- **Không commit `.env` / API key** (−10 điểm). Không mã học viên `L0000`, không nguyên file data BTC.
- Phỏng vấn dùng mã P1, P2…, không tên thật.
- Kẹt quá 20 phút → báo nhóm.

---

## Trà — toàn bộ phần bằng chứng + impact

| Việc | Ra file | Xong khi |
|---|---|---|
| Ghi mọi cuộc phỏng vấn nhóm đã làm (đã có P1; ai đã hỏi thêm thì kể lại để Trà ghi P2, P3…) | `evidence/interviews/P*.md` | Mỗi file có trích nguyên văn |
| Viết `evidence/summary.md`: số chính (lấy từ `evidence/data-mining.md`) + ≥5 trích dẫn / ví dụ + kết luận pain | `evidence/summary.md` | Đủ ≥5 trích dẫn / ví dụ, mỗi cái có nguồn |
| Điền bảng impact `spec.md` §2: số giảng viên × số buổi / tháng × số phút tiết kiệm; thiếu nguồn ghi *(tự ước tính)* | `spec.md` §2 | Mỗi thừa số có nguồn |
| Điền dòng bằng chứng `spec.md` §1 ("Bằng chứng — số chính + kết luận") | `spec.md` §1 | Khớp `summary.md` |

## Duy — toàn bộ phần AI chạy thật + video

| Việc | Ra file | Xong khi |
|---|---|---|
| Lấy API key → `.env`. Viết nhánh gọi model thật trong `call_model` (giữ 4 khoá, token lấy từ `usage`) theo `docs/connect-model.md` | `codebase/ai.py` | `python run.py eval --try` ra token > 0 |
| Chạy `Ngày 1`, `Ngày 5`, câu `d05-on-cot-canvas` với model thật; phần AI bị lớp kiểm chặn (số lạ, mã lạ) thì sửa `SYSTEM` prompt cho tới khi ra | `codebase/agent.py` | Phần D hiện ra ở ngày 1–5 |
| Sửa dòng "Phần nào còn giả" ở `spec.md` §4 cho đúng trạng thái mới | `spec.md` §4 | |
| Quay **video 30 giây**: gõ "Ngày 5 lớp vướng gì?" → thẻ có AI thật | link YouTube không công khai / Drive | Mở được bằng cửa sổ ẩn danh |

## Hiếu — toàn bộ phần dữ liệu + đánh giá

| Việc | Ra file | Xong khi |
|---|---|---|
| Đẩy PR `DATA_CARD.md` + `question_bank.csv` | PR | Có đề các câu bị gắn cờ (`d05-on-cot-canvas`, `d01-on-chatbot-la-ung-dung`, `d03-on-tong-5-diem`, `d04-on-cot-hai`, `d02-on-can-agent`…) |
| **Thêm** câu thử B15 trở đi lên **20–30 câu** (ngày khác, mã câu khác, câu chưa có đề, vài câu từ lời phỏng vấn `nguoi_dung: P1`). **Không sửa B01–B14** | `eval/benchmark.csv` | `python run.py check` hết cảnh báo |
| Cập nhật `spec.md` §7 dòng số câu (thuong / kho / tu_choi) | `spec.md` §7 | Khớp `benchmark.csv` |
| Sáng mai: tự chạy **lượt 1** `python run.py eval` (dùng `.env` của mình — key nhóm Duy gửi riêng, không qua repo) → chấm cột `pass` → `python run.py score eval/run-1.csv` → commit | `eval/run-1.csv` | Có run ID, token, % đạt |

## Nam — spec + điều phối + nộp

| Việc | Ra file | Xong khi |
|---|---|---|
| Điền `spec.md` §0, §1 (trừ dòng bằng chứng), §3, §5, §6 | `spec.md` | §0–§7 không còn `__` |
| Gộp PR của cả nhóm trước khi ngủ; kiểm `python run.py check` trên `main` | — | `main` đủ mọi phần |
| Sáng mai: soát checklist, điền form, **nộp CP3** | form CP3 | Nộp trước 10:00 |

---

## Thứ tự

Bốn phần làm **song song từ bây giờ**, không ai chờ ai. Chỉ có 2 mốc chung:

1. **23:00** — mọi PR đã gộp vào `main` (câu thử đã đủ 20–30 câu, Duy đã gọi được model).
2. **9:00 sáng mai** — Hiếu chạy lượt 1 trên `main` và chấm; Duy quay video. **9:45** Nam soát. **10:00** nộp.

Mỗi người sửa một phần riêng của `spec.md` (Trà §1 bằng chứng + §2 · Duy §4 dòng "còn giả" · Hiếu §7 dòng số câu · Nam phần còn lại) → git tự gộp được, ít đụng nhau.

**Lượt 1 thấp là bình thường.** Không sửa `expected`, không bỏ câu trượt, không đổi chuẩn "đạt".
