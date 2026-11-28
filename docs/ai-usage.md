# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm / sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Claude Code (Nam), Codex (Duy) | Viết khung `agent.py`, `tools.py` (luồng cố định, 3 công cụ chỉ đọc, regex từ chối, lớp kiểm đầu ra); nối API trong `ai.py`; viết giao diện Streamlit và test `tests/`, `validation/test_*.py` | Chạy tay bằng `--cli` các câu B01–B24 trước lượt chạy. Chọn ngưỡng (10 lượt, 30%, 50%) bằng số trong data. Sau lượt 2 thấy `_loc_synthetic` quá cứng làm `thuong` 0/8 (`eval/report.md` §3) | Nam (khung), Duy (model, giao diện, bản sửa CP4) |
| Prompt / thiết kế lời gọi model | Claude Code, Codex | Soạn `SYSTEM` prompt (không tự đếm, không nhắc học viên, đề `synthetic` chỉ là câu hỏi ví dụ) | Không tin prompt: mọi giới hạn quan trọng đều có code chặn (`TU_CHOI`, `_kiem_dau_ra_ai`, `_loc_synthetic`) | Duy |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code | Viết `evidence/count_review.py`, `count_struggle.py` theo cách đếm viết trước trong `data-mining.md` §1 | Đọc dòng đầu các file và `column_dictionary.csv` trước khi đếm. Đối chiếu 6/6 ví dụ ở `data-mining.md` §4 với CSV đầu ra (khớp cả 6). Sửa 2 chỗ AI làm sai: ngưỡng mẫu 20 → 10 (nhiều ngày không đủ mẫu), ghép 208/453 dòng lab trống `kc_code` bằng `lesson_id` + `lab_key` | Nam |
| Rà câu hỏi phỏng vấn | Claude Code | Chỉ rà câu dẫn dắt theo Mom Test | Câu hỏi và ghi chép P1 do người làm. Trích dẫn lấy nguyên văn từ ghi âm, AI không viết | Trà, Nam |
| Tổng hợp bằng chứng, impact, chi phí | Claude Code | Đối chiếu số trong `evidence/summary.md` với `data/*.csv`, soạn `cost/personas.yaml`, chạy `simulate` | Không dùng số chi phí AI tự ước. Số nộp lấy nguyên từ `cost/simulate-1-summary.md`. Thừa số không có nguồn ghi *(tự ước tính)* | Trà |
| Viết câu thử (benchmark) | Có dùng AI (Hiếu ghi tên công cụ) | Gợi ý câu khó / tấn công | Mỗi câu có `source`. 18/24 câu từ người dùng hoặc data thật (`run.py check`). B01–B14 không đổi sau CP2 | Hiếu |
| Sinh data `synthetic` | Có dùng AI (Hiếu ghi tên công cụ) | Soạn 19 đề ở `data/question_bank.csv` theo `ref` / `kc_code` (pre-class không còn đề gốc) | Kiểm tay 19/19 dòng (`eval/README.md` §1). Nhãn `synthetic`, không dùng làm bằng chứng. Sửa lỗi mã hoá ANSI ở bản PR đầu | Hiếu |
| Chấm cột `pass` bằng LLM | Không dùng | — | Hiếu chấm tay 24/24 câu mỗi lượt theo `pass_criterion` và `metric_spec.yaml` | Hiếu |
| Slide, văn bản | Claude Code | Soạn nháp spec §0–§10, slide 8 trang, kịch bản demo | Mọi số trên slide trỏ về file nguồn. Câu nào không có nguồn thì bỏ | Nam |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
