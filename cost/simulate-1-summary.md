# Tóm tắt mô phỏng simulate-1@20261128-113444

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| gv_chi_doc_the | 24 | 1 | 1589 | 504 | 1.0 | 3.1 |
| gv_hoi_tiep | 19 | 3 | 3144 | 967 | 2.1 | 7.1 |
| phu_trach_nhieu_lop | 7 | 2 | 1640 | 450 | 1.3 | 4.0 |

Tỉ lệ đạt dùng để tính: 15/24 (62%) — lượt run-2@20261128-101829

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (3 người) | Chi phí / tháng — cơ sở (5 người) | Chi phí / tháng — cao (10 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-5.4-nano (vào 0.2 · ra 1.25 $/1M) | $0.0013 | $0.0020 | $0.0011 | $0.0822 | $0.1370 | $0.2740 | $0.0274 |
| gpt-5.4-mini (vào 0.75 · ra 4.5 $/1M) | $0.0047 | $0.0075 | $0.0039 | $0.3002 | $0.5003 | $1.00 | $0.1001 |
| gpt-5.4 (vào 2.5 · ra 15.0 $/1M) | $0.0156 | $0.0249 | $0.0131 | $1.00 | $1.67 | $3.34 | $0.3336 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.9) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5.4-nano. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
