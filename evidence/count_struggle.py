"""Đào data "điểm nghẽn" theo từng phần bài (module) — Class Pulse · AI4FUN.

Gom mọi tín hiệu học viên đang sai / khó hiểu / nghẽn trong pre-class, theo module_code (<bài>:module-N):
    1. Bài ôn cuối ngày (answers.csv, nguon = pre_post_post, lan_thu = 1): lượt sai / lượt trả lời
    2. Bước thực hành (answers.csv, nguon = thuc_hanh, lan_thu = 1): lượt sai / lượt làm
       + bài thực hành bị bấm bỏ qua (events.csv, lab_completed, data.skipped = true) / lượt kết thúc lab
    3. Hỏi trợ giảng dưới video (chat.csv, channel = video_question): số câu hỏi / số học viên đã mở video đó
       video → module lấy từ events.csv (dòng có cả video và kc_code)
    4. Bôi đen chữ trên slide để hỏi (events.csv, slide_text_asked): số lượt, theo module và số slide
Không dùng: câu hỏi giữa video (chỉ 7 lượt có chấm đúng/sai) · lượt tua video (không tách được tua tay với tự nhảy).

Chạy lại (chỉ thư viện chuẩn):
    python -I evidence/count_struggle.py <thư mục data/preclass của repo đề>
Đầu ra: in bảng tổng · ghi data/struggle_by_module.csv (chỉ số đã tổng hợp, không có mã học viên).
"""
import collections
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "struggle_by_module.csv")


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pct(x, n):
    return round(x / n, 3) if n else ""


def main(d):
    answers = read(os.path.join(d, "answers.csv"))
    chat = read(os.path.join(d, "chat.csv"))

    M = collections.defaultdict(lambda: collections.Counter())
    lesson_of = {}
    video_module = collections.defaultdict(collections.Counter)
    video_viewers = collections.defaultdict(set)
    slides = collections.defaultdict(collections.Counter)

    for a in answers:
        mod = a["module_code"]
        if not mod or a["lan_thu"] != "1" or a["was_correct"] not in ("True", "False"):
            continue
        lesson_of[mod] = a["lesson_id"]
        if a["nguon"] in ("pre_post_post", "thuc_hanh"):
            key = "on" if a["nguon"] == "pre_post_post" else "th"
            M[mod][key + "_n"] += 1
            M[mod][key + "_sai"] += a["was_correct"] == "False"

    with open(os.path.join(d, "events.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            t, mod = r["type"], r["kc_code"]
            if r["video"] and mod.count(":module-"):
                video_module[r["video"]][mod] += 1
            if t == "video_opened" and r["video"]:
                video_viewers[r["video"]].add(r["hv"])
            if t == "lab_completed":
                dd = json.loads(r["data"] or "{}")
                if not mod and r["lesson_id"] and dd.get("lab_key"):  # 208/453 dòng lab trống kc_code
                    mod = "%s:lab-%s" % (r["lesson_id"], dd["lab_key"])
            if not mod.startswith("program-"):
                continue
            if t == "lab_completed":
                lesson_of.setdefault(mod, r["lesson_id"])
                M[mod]["lab_n"] += 1
                M[mod]["lab_bo_qua"] += bool(dd.get("skipped"))
            elif t == "slide_text_asked":
                lesson_of.setdefault(mod, r["lesson_id"])
                dd = json.loads(r["data"] or "{}")
                M[mod]["boi_slide"] += 1
                slides[mod][dd.get("slide")] += 1

    vid2mod = {v: c.most_common(1)[0][0] for v, c in video_module.items()}
    viewers_by_mod = collections.defaultdict(set)
    for v, hv in video_viewers.items():
        if v in vid2mod:
            viewers_by_mod[vid2mod[v]] |= hv
    for c in chat:
        if c["channel"] != "video_question":
            continue
        v = os.path.splitext(os.path.basename(c["transcript"]))[0]
        if v in vid2mod:
            M[vid2mod[v]]["hoi_ta"] += 1
            lesson_of.setdefault(vid2mod[v], "")

    rows = []
    for mod, c in M.items():
        nv = len(viewers_by_mod.get(mod, ()))
        top_slide = slides[mod].most_common(1)
        rows.append({
            "module_code": mod,
            "lesson_id": lesson_of.get(mod) or mod.rsplit(":", 1)[0],
            "on_n": c["on_n"], "on_sai": c["on_sai"], "on_ti_le_sai": pct(c["on_sai"], c["on_n"]),
            "th_n": c["th_n"], "th_sai": c["th_sai"], "th_ti_le_sai": pct(c["th_sai"], c["th_n"]),
            "lab_n": c["lab_n"], "lab_bo_qua": c["lab_bo_qua"], "lab_ti_le_bo_qua": pct(c["lab_bo_qua"], c["lab_n"]),
            "hv_mo_video": nv, "hoi_ta": c["hoi_ta"], "hoi_ta_moi_hv": pct(c["hoi_ta"], nv),
            "boi_slide": c["boi_slide"],
            "slide_hoi_nhieu_nhat": top_slide[0][0] if top_slide else "",
            "so_lan_slide_do": top_slide[0][1] if top_slide else 0,
        })
    rows.sort(key=lambda r: r["module_code"])
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    S = lambda k: sum(r[k] for r in rows)
    print("Module có tín hiệu: %d" % len(rows))
    print("Bài ôn lần đầu sai: %d/%d (%.1f%%)" % (S("on_sai"), S("on_n"), 100 * S("on_sai") / S("on_n")))
    print("Bước thực hành lần đầu sai: %d/%d (%.1f%%)" % (S("th_sai"), S("th_n"), 100 * S("th_sai") / S("th_n")))
    print("Lab bấm bỏ qua: %d/%d (%.1f%%)" % (S("lab_bo_qua"), S("lab_n"), 100 * S("lab_bo_qua") / S("lab_n")))
    print("Câu hỏi trợ giảng dưới video gắn được module: %d/%d" % (
        S("hoi_ta"), sum(1 for c in chat if c["channel"] == "video_question")))
    print("Lượt bôi đen slide để hỏi: %d" % S("boi_slide"))
    print("\nTop 8 module theo số câu hỏi trợ giảng / học viên mở video (>= 10 học viên):")
    for r in sorted([r for r in rows if r["hv_mo_video"] >= 10], key=lambda r: -r["hoi_ta_moi_hv"])[:8]:
        print("  %-62s %3d câu / %3d hv (%.2f)" % (r["module_code"], r["hoi_ta"], r["hv_mo_video"], r["hoi_ta_moi_hv"]))
    print("\nTop 5 lab bị bỏ qua nhiều (>= 10 lượt):")
    for r in sorted([r for r in rows if r["lab_n"] >= 10], key=lambda r: -r["lab_ti_le_bo_qua"])[:5]:
        print("  %-62s %3d/%-3d (%.0f%%)" % (r["module_code"], r["lab_bo_qua"], r["lab_n"], 100 * r["lab_ti_le_bo_qua"]))
    print("\nTop 5 module bôi đen slide nhiều:")
    for r in sorted(rows, key=lambda r: -r["boi_slide"])[:5]:
        print("  %-62s %3d lượt · slide %s: %d" % (r["module_code"], r["boi_slide"], r["slide_hoi_nhieu_nhat"], r["so_lan_slide_do"]))
    print("\nĐã ghi %s (%d module)" % (os.path.relpath(OUT), len(rows)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
