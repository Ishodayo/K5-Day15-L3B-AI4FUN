"""Công cụ của bài toán — Class Pulse · AI4FUN. Khớp bảng công cụ ở spec.md §4.

Mọi công cụ chỉ ĐỌC số đã tổng hợp trong data/ (do evidence/count_review.py và evidence/count_struggle.py
tính từ data pre-class BTC cấp). Không công cụ nào gửi tin, sửa bài, hay chấm học viên.
"""
import csv
import os

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

MIN_N = 10          # ngưỡng mẫu: lượt trả lời lần đầu tối thiểu của một câu ôn / bước thực hành / lab
SAI_CAO = 0.30      # tỉ lệ sai lần đầu coi là cao
DON_DAP_AN = 0.50   # >= 50% lượt sai dồn vào cùng một đáp án → dấu hiệu hiểu sai chung / câu gây nhầm
BO_QUA_CAO = 0.30   # tỉ lệ bấm bỏ qua lab coi là cao
HOI_TA_CAO = 0.40   # số câu hỏi trợ giảng / học viên mở video coi là cao


def _read(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _day(lesson_or_ref):
    """'program-day05:...' hoặc 'd05-on-...' → 5; không đọc được → None."""
    s = lesson_or_ref or ""
    if s.startswith("program-day"):
        s = s[len("program-day"):]
    elif s.startswith("d"):
        s = s[1:]
    digits = s[:2]
    return int(digits) if digits.isdigit() else None


@tool
def lay_tin_hieu_ngay(ngay: int) -> dict:
    """lay_tin_hieu_ngay — số tổng hợp các điểm nghẽn của một ngày học.
    Input: ngay (int, 1–13). Output: {"ngay", "cau_on": [...], "module": [...]} — mỗi câu ôn có
    n_lan_dau, sai_lan_dau, ti_le_sai, dap_an_sai_nhieu_nhat, so_chon_dap_an_do, sai_co_dap_an, du_mau;
    mỗi module có số sai thực hành, lab bỏ qua, câu hỏi trợ giảng / học viên, lượt bôi đen slide.
    Không có dữ liệu ngày đó → hai danh sách rỗng. Không tác động ra ngoài (chỉ đọc data/)."""
    q = [r for r in _read("review_stats.csv") if _day(r["lesson_id"]) == ngay]
    m = [r for r in _read("struggle_by_module.csv") if _day(r["lesson_id"]) == ngay]
    return {"ngay": ngay, "cau_on": q, "module": m}


@tool
def lay_tin_hieu_cau(ref: str) -> dict:
    """lay_tin_hieu_cau — số tổng hợp của MỘT câu ôn theo mã câu (vd d01-on-chatbot-la-ung-dung).
    Input: ref (str). Output: dòng số liệu của câu đó, hoặc {} nếu mã không có trong data.
    Không tác động ra ngoài."""
    for r in _read("review_stats.csv"):
        if r["ref"] == ref:
            return r
    return {}


@tool
def lay_de_cau_hoi(ref: str) -> dict:
    """lay_de_cau_hoi — đề, các đáp án, đáp án đúng và đoạn bài liên quan của một câu ôn
    (data/question_bank.csv, nhóm chép / viết lại từ pre-class).
    Input: ref (str). Output: {"ref","de","cac_dap_an","dap_an_dung","doan_bai"} hoặc {} nếu chưa có đề.
    Không tác động ra ngoài."""
    for r in _read("question_bank.csv"):
        if r.get("ref") == ref and (r.get("de") or "").strip():
            return r
    return {}


def danh_gia_cau(r: dict) -> dict:
    """Code (không phải AI) gắn nhãn sơ bộ cho một câu ôn từ số liệu. AI chỉ diễn giải nhãn này."""
    n, sai = int(r["n_lan_dau"]), int(r["sai_lan_dau"])
    co_da, don = int(r["sai_co_dap_an"] or 0), int(r["so_chon_dap_an_do"] or 0)
    ti_le = sai / n if n else 0
    if n < MIN_N:
        nhan = "chua_du_du_lieu"
    elif co_da >= 5 and don / co_da >= DON_DAP_AN and ti_le >= 0.2:
        nhan = "sai_don_mot_dap_an"   # hiểu sai chung HOẶC câu hỏi gây nhầm — AI + giảng viên phân biệt
    elif ti_le >= SAI_CAO:
        nhan = "sai_cao_rai_rac"
    else:
        nhan = "khong_can_on"
    return {"ref": r["ref"], "kc_code": r["kc_code"], "n": n, "sai": sai, "ti_le": ti_le,
            "dap_an": r["dap_an_sai_nhieu_nhat"], "don": don, "co_da": co_da, "nhan": nhan}


def danh_gia_module(r: dict) -> list:
    """Code gắn cờ cho một module: lab bỏ qua nhiều, hỏi trợ giảng nhiều. Trả danh sách cờ (có thể rỗng)."""
    co = []
    lab_n, bq = int(r["lab_n"]), int(r["lab_bo_qua"])
    if lab_n >= MIN_N and bq / lab_n >= BO_QUA_CAO:
        co.append("lab bị bỏ qua %d/%d lượt (%.0f%%)" % (bq, lab_n, 100 * bq / lab_n))
    th_n, th_sai = int(r["th_n"]), int(r["th_sai"])
    if th_n >= MIN_N and th_sai / th_n >= SAI_CAO:
        co.append("bước thực hành sai lần đầu %d/%d (%.0f%%)" % (th_sai, th_n, 100 * th_sai / th_n))
    hv, hoi = int(r["hv_mo_video"]), int(r["hoi_ta"])
    if hv >= MIN_N and hoi / hv >= HOI_TA_CAO:
        co.append("%d câu hỏi trợ giảng / %d học viên mở video (%.2f câu/người)" % (hoi, hv, hoi / hv))
    if int(r["so_lan_slide_do"] or 0) >= MIN_N:
        co.append("slide %s được bôi đen để hỏi %s lượt" % (r["slide_hoi_nhieu_nhat"], r["so_lan_slide_do"]))
    return co
