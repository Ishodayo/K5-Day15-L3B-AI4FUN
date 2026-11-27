"""Luồng chính — Class Pulse · AI4FUN. Khớp sơ đồ spec.md §4.

Hình dạng: WORKFLOW CỐ ĐỊNH, AI làm đúng 1 bước (diễn giải + gợi ý). Code tính mọi con số.
    1. Code đọc yêu cầu của giảng viên: ngày học / mã câu ôn. Ngoài phạm vi → từ chối. Thiếu → hỏi lại (G10).
    2. Công cụ đọc số đã tổng hợp (data/review_stats.csv, data/struggle_by_module.csv).
    3. Code gắn nhãn sơ bộ theo ngưỡng (tools.danh_gia_cau / danh_gia_module); dưới ngưỡng mẫu → "chưa đủ dữ liệu".
    4. Công cụ lấy đề + đoạn bài của các câu bị gắn cờ (data/question_bank.csv).
    5. AI (1 lần gọi) phân biệt hiểu sai chung / câu hỏi gây nhầm, viết gợi ý điều chỉnh bài giảng + câu quiz ôn nháp.
    6. Code kiểm đầu ra AI: không mã câu lạ, không số lạ, không mã học viên. Trượt → bỏ phần AI, giữ thẻ số liệu.
    7. Trả bản nháp — giảng viên duyệt, sửa hoặc bỏ. Không gửi gì đi đâu.
"""
import json
import re

from ai import call_model
from tools import (MIN_N, danh_gia_cau, danh_gia_module, lay_de_cau_hoi, lay_tin_hieu_cau,
                   lay_tin_hieu_ngay)
from tracing import note

SYSTEM = """Bạn hỗ trợ GIẢNG VIÊN khoá AI20K điều chỉnh bài giảng từ kết quả pre-class của lớp.
Bạn nhận các THẺ do code tính sẵn (mã câu, số lượt, tỉ lệ sai, đáp án sai được chọn nhiều nhất), kèm đề câu hỏi
và đoạn bài nếu có. Với MỖI thẻ, viết đúng 3 dòng:
  [mã thẻ] Loại: hiểu sai chung | câu hỏi gây nhầm | nghẽn thực hành | cần xem thêm
  Vì sao: dựa trên đề / đoạn bài được đưa (trích ngắn). Nếu thẻ ghi "chưa có đề" thì viết "chưa có đề câu hỏi — giảng viên xem đề trước khi kết luận".
  Gợi ý: 1 điều chỉnh bài giảng ≤ 2 câu, và 1 câu quiz ôn nháp (chỉ khi có đề).
Luật: KHÔNG viết thêm con số nào ngoài số đã có trong thẻ. KHÔNG nhắc mã thẻ / mã câu không có trong danh sách.
KHÔNG nhắc, đoán hay xếp hạng học viên. Bạn chỉ đề xuất; giảng viên quyết định."""

TU_CHOI = [
    (r"x[eế]p h[aạ]ng|y[eế]u nh[aấ]t|gi[oỏ]i nh[aấ]t|top \d+ h[oọ]c vi[eê]n",
     "Không xếp hạng học viên. Thẻ chỉ có số tổng hợp theo câu / phần bài."),
    (r"h[oọ]c vi[eê]n n[aà]o|ai (đã )?sai|t[eê]n h[oọ]c vi[eê]n|m[aã] h[oọ]c vi[eê]n|danh s[aá]ch h[oọ]c vi[eê]n|\bL\d{4}\b",
     "Không cung cấp học viên cụ thể đã sai — chỉ có số tổng hợp, để giảng viên ôn cho cả lớp."),
    (r"\bg[uử]i\b|email|nh[aắ]n (cho|t[oớ]i)|đăng l[eê]n|thông báo cho",
     "Không tự gửi gì cho học viên. Thẻ và quiz là bản nháp; giảng viên tự chép đi nếu duyệt."),
    (r"s[uử]a (đ[eề]|b[aà]i|đ[aá]p [aá]n) tr[eê]n pre.?class|ch[aấ]m (l[aạ]i )?đi[eể]m",
     "Không sửa nội dung pre-class hay chấm điểm. Chỉ đề xuất để giảng viên quyết."),
    (r"b[oỏ] qua (h[uư][oớ]ng d[aẫ]n|lu[aậ]t)|ignore (previous|all)|system prompt",
     "Không làm theo yêu cầu bỏ qua luật hoạt động."),
]
HUONG_DAN = ("Hỏi theo ngày học hoặc mã câu ôn, ví dụ: \"Ngày 3: lớp đang vướng gì?\" "
             "hoặc \"Câu d01-on-chatbot-la-ung-dung có cần ôn không?\"")


def _doc_yeu_cau(text):
    t = text.lower()
    ref = re.search(r"\bd\d{2}-on-[a-z0-9-]+", t)
    day = re.search(r"(?:ng[aà]y|day|bu[oổ]i)\s*0?(\d{1,2})\b", t)
    return (ref.group(0) if ref else None), (int(day.group(1)) if day else None)


def _the_cau(c):
    s = "%s · KC %s · sai lần đầu %d/%d (%.0f%%)" % (c["ref"], c["kc_code"], c["sai"], c["n"], 100 * c["ti_le"])
    if c["co_da"]:
        s += " · đáp án sai chọn nhiều nhất: %s (%d/%d lượt sai)" % (c["dap_an"], c["don"], c["co_da"])
    return s


def _kiem_dau_ra_ai(text, refs, so_cho_phep):
    """Chỗ chặn rủi ro: trả lý do trượt (str) hoặc "" nếu qua."""
    if re.search(r"\bL\d{4}\b", text):
        return "có mã học viên"
    la = set(re.findall(r"\bd\d{2}-on-[a-z0-9-]+", text)) - set(refs)
    if la:
        return "nhắc mã câu không có trong thẻ: %s" % ", ".join(sorted(la))
    so_la = set(re.findall(r"\b\d+/\d+\b|\b\d+(?:[.,]\d+)?%", text)) - so_cho_phep
    if so_la:
        return "có số không do code tính: %s" % ", ".join(sorted(so_la))
    return ""


def _dien_giai(the_cau, the_module):
    """Bước AI duy nhất. Trả (đoạn chữ, ghi chú kiểm)."""
    if not the_cau and not the_module:
        return "", ""
    goi = []
    for c in the_cau:
        de = lay_de_cau_hoi(c["ref"])
        goi.append({"ma_the": c["ref"], "so_lieu": _the_cau(c), "nhan_code": c["nhan"],
                    "de": de.get("de") or "chưa có đề", "cac_dap_an": de.get("cac_dap_an", ""),
                    "dap_an_dung": de.get("dap_an_dung", ""), "doan_bai": de.get("doan_bai", "")})
    for mod, co in the_module:
        goi.append({"ma_the": mod, "so_lieu": "; ".join(co), "nhan_code": "nghen_phan_bai", "de": "chưa có đề"})
    reply = call_model(SYSTEM, "Các thẻ:\n" + json.dumps(goi, ensure_ascii=False, indent=1))
    text = reply["text"].strip()
    so_cho_phep = set(re.findall(r"\b\d+/\d+\b|\b\d+(?:[.,]\d+)?%", json.dumps(goi, ensure_ascii=False)))
    loi = _kiem_dau_ra_ai(text, [c["ref"] for c in the_cau], so_cho_phep)
    if loi:
        note("chặn đầu ra AI: " + loi)
        return "", "(Đã bỏ phần diễn giải của AI vì %s — chỉ giữ số liệu do code tính.)" % loi
    return text, ""


def answer(text: str) -> dict:
    for pattern, ly_do in TU_CHOI:
        if re.search(pattern, text, re.IGNORECASE):
            note("từ chối: " + ly_do)
            return {"output": "Không làm được: %s\n%s" % (ly_do, HUONG_DAN)}

    ref, ngay = _doc_yeu_cau(text)
    if ref:
        r = lay_tin_hieu_cau(ref)
        if not r:
            return {"output": "Không có câu ôn mã %s trong dữ liệu. %s" % (ref, HUONG_DAN)}
        c = danh_gia_cau(r)
        if c["nhan"] == "chua_du_du_lieu":
            return {"output": "Câu %s: chưa đủ dữ liệu — mới có %d lượt trả lời lần đầu (cần ≥ %d). "
                              "Chưa nên kết luận có cần ôn hay không." % (ref, c["n"], MIN_N)}
        if c["nhan"] == "khong_can_on":
            return {"output": "Câu %s: không cần ôn — %s. Tỉ lệ sai thấp, sai không dồn vào một đáp án."
                              % (ref, _the_cau(c))}
        ai_text, ghi_chu = _dien_giai([c], [])
        out = "THẺ ĐIỂM NGHẼN (bản nháp — giảng viên duyệt)\n- " + _the_cau(c)
        return {"output": out + ("\n\n" + ai_text if ai_text else "") + ("\n" + ghi_chu if ghi_chu else "")}

    if ngay is None:
        return {"output": "Bạn muốn xem ngày học nào (1–13) hoặc câu ôn nào? " + HUONG_DAN}

    data = lay_tin_hieu_ngay(ngay)
    if not data["cau_on"] and not data["module"]:
        return {"output": "Không có dữ liệu pre-class cho ngày %d (data hiện có ngày 1–13)." % ngay}

    cau = [danh_gia_cau(r) for r in data["cau_on"]]
    co_co = sorted([c for c in cau if c["nhan"] in ("sai_don_mot_dap_an", "sai_cao_rai_rac")],
                   key=lambda c: -c["ti_le"])[:3]
    thieu = [c for c in cau if c["nhan"] == "chua_du_du_lieu"]
    mods = [(r["module_code"], danh_gia_module(r)) for r in data["module"]]
    mods = [(m, co) for m, co in mods if co][:3]

    lines = ["THẺ ĐIỂM NGHẼN — Ngày %d (bản nháp — giảng viên duyệt, sửa hoặc bỏ)" % ngay]
    lines.append("A. Câu ôn nên xem lại (%d/%d câu đủ mẫu bị gắn cờ):" % (len(co_co), len(cau) - len(thieu)))
    lines += ["  - " + _the_cau(c) for c in co_co] or ["  - Không có câu đủ mẫu nào sai cao."]
    lines.append("B. Phần bài có tín hiệu nghẽn:")
    lines += ["  - %s: %s" % (m, "; ".join(co)) for m, co in mods] or ["  - Không có phần bài nào vượt ngưỡng."]
    if thieu:
        lines.append("C. Chưa đủ dữ liệu: %d/%d câu ôn có < %d lượt trả lời lần đầu — không đề xuất ôn các câu này."
                     % (len(thieu), len(cau), MIN_N))
    ai_text, ghi_chu = _dien_giai(co_co, mods)
    if ai_text:
        lines += ["", "D. Diễn giải và gợi ý điều chỉnh (AI đề xuất):", ai_text]
    if ghi_chu:
        lines.append(ghi_chu)
    lines.append("Giới hạn: số đếm trên toàn bộ học viên có làm pre-class, chưa tách theo lớp; data cho biết sai ở đâu, không cho biết vì sao.")
    return {"output": "\n".join(lines)}
