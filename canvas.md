# Canvas — AI4FUN · Track A

> Điền ở guide bước 1.4. CP1 17:00 Thứ Sáu 27/11: nộp bản đầu, đủ 7 dòng (dòng 4 được ghi giả thuyết + nguồn sẽ kiểm).
> CP2 19:30 Thứ Sáu 27/11: cập nhật (số bằng chứng đầu, lát cắt đã chốt) và điền dòng "Đã đổi gì so với CP1".

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | **Track A · EdTech — Class Pulse:** thẻ "điểm nghẽn kiến thức" của lớp từ kết quả bài ôn cuối ngày trên pre-class, giúp người phụ trách buổi học chọn đúng 1–3 ý cần ôn đầu buổi sau |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | **Lab coach / TA phụ trách một buổi học của lớp L3**, người chuẩn bị phần ôn đầu buổi tiếp theo |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Lab coach/TA chuẩn bị buổi học tiếp theo **không biết ý kiến thức nào cả lớp đang hiểu sai** sau bài pre-class, vì kết quả bài ôn nằm rải rác theo từng học viên; phần ôn đầu buổi chọn theo cảm tính, nên có ý cả lớp hiểu sai mà không ai sửa (học viên làm sai gần như không làm lại) |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm · CP2: số đầu tiên + 1 trích dẫn | **Giả thuyết:** người phụ trách buổi học hiện không có cách nhanh để biết lớp hiểu sai ý nào; có những ý mà nhiều học viên sai cùng một kiểu. **Tín hiệu đầu từ data pre-class (đếm sơ bộ, sẽ viết script kiểm lại):** 399/1.968 lượt trả lời bài ôn lần đầu sai (20,3%) · câu `d01-on-chatbot-la-ung-dung`: 16/41 sai, trong đó 9/16 chọn cùng đáp án C · chỉ 2/424 lượt sai lần đầu có làm lại. **Nguồn sẽ kiểm:** (1) đào data `data/preclass` theo từng câu hỏi / ý kiến thức, có script trong repo; (2) phỏng vấn ≥3 lab coach/TA: "buổi gần nhất, bạn biết lớp đang vướng ý nào bằng cách nào, mất bao lâu?"; (3) phỏng vấn ≥3 học viên về các câu sai nhiều nhất |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | **Một lab coach · tối trước buổi học tiếp theo · AI đọc thống kê bài ôn (tỉ lệ sai lần đầu, đáp án sai được chọn nhiều nhất — do code tính) cùng đề câu hỏi và đoạn bài, quyết định mỗi ý là *hiểu sai chung / câu hỏi gây nhầm / chưa đủ dữ liệu / không cần ôn* kèm 1 hoạt động ôn 3 phút · coach chọn đúng 1–3 ý để ôn đầu buổi** |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | AI **chỉ đề xuất** thẻ; coach duyệt, sửa hoặc bỏ. Không gửi thông báo, không sửa bài, không chấm hay xếp hạng học viên. Mọi con số do code tính; dưới ngưỡng mẫu thì trả "chưa đủ dữ liệu". **Sai thì:** ôn nhầm ý (lớp mất vài phút) hoặc bỏ sót ý cả lớp hiểu sai (học viên mang hiểu lầm sang bài sau) — nên coach là người quyết định cuối |
| 7 | Phân công có tên | **Nguyễn Thành Nam** (đội trưởng): điều phối, spec, kiến trúc, slide · **Phùng Quang Trà:** phỏng vấn lab coach/TA và học viên, impact · **Lê Hiền Hiếu:** đào data pre-class, data card, bộ câu thử, metric · **Đặng Quang Duy:** bản chạy thử, gọi model, mô phỏng chi phí |
| — | *(CP2)* Đã đổi gì so với CP1 | |
