"""Đào data bài ôn cuối ngày (pre_post_post) theo từng câu hỏi — Class Pulse · AI4FUN.

Chạy lại (chỉ thư viện chuẩn):
    python -I evidence/count_review.py <thư mục data/preclass của repo đề>
    vd: python -I evidence/count_review.py ../Reference/K5-L3-Day15-AI-Product-Hackathon/data/preclass

Đầu ra:
    - in bảng tổng ra màn hình
    - ghi data/review_stats.csv: số đã tổng hợp theo câu (không có mã học viên) — công cụ của bản chạy thử đọc file này

Cách đếm (viết trước khi chạy, xem evidence/data-mining.md §1):
    - Tập: answers.csv, nguon = pre_post_post (bài ôn cuối ngày), lan_thu = 1 (lần đầu), was_correct là True/False.
    - Mẫu số của tỉ lệ sai một câu: số lượt trả lời lần đầu của câu đó.
    - Đáp án đã chọn: lấy khoá "chosen" trong cột data của events.csv (type = answer_submitted), nối qua ref_id = answers.id.
    - Làm lại sau khi sai: cùng học viên, cùng câu, có lượt lan_thu >= 2.
    - Ngưỡng mẫu: câu có < MIN_N lượt lần đầu bị gắn "chua_du_du_lieu".
"""
import collections
import csv
import json
import os
import sys

MIN_N = 10  # ngưỡng mẫu: số lượt trả lời lần đầu tối thiểu của một câu (lớp ~40 người, ngày sau ít người làm)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "data", "review_stats.csv")


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main(data_dir):
    answers = read(os.path.join(data_dir, "answers.csv"))
    chosen = {}
    with open(os.path.join(data_dir, "events.csv"), encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["type"] != "answer_submitted" or not r["ref_id"]:
                continue
            try:
                d = json.loads(r["data"] or "{}")
            except ValueError:
                continue
            if d.get("chosen") is not None:
                chosen[r["ref_id"]] = str(d["chosen"])

    review = [a for a in answers if a["nguon"] == "pre_post_post" and a["was_correct"] in ("True", "False")]
    first = [a for a in review if a["lan_thu"] == "1"]
    retried = {(a["hv"], a["ref"]) for a in review if a["lan_thu"] not in ("", "1")}

    by_q = collections.defaultdict(list)
    for a in first:
        by_q[a["ref"]].append(a)

    rows = []
    for ref, items in by_q.items():
        n = len(items)
        wrong = [a for a in items if a["was_correct"] == "False"]
        opts = collections.Counter(chosen[a["id"]] for a in wrong if a["id"] in chosen)
        top, top_n = (opts.most_common(1)[0] if opts else ("", 0))
        rows.append({
            "ref": ref,
            "lesson_id": items[0]["lesson_id"],
            "kc_code": items[0]["kc_code"],
            "n_lan_dau": n,
            "n_hoc_vien": len({a["hv"] for a in items}),
            "sai_lan_dau": len(wrong),
            "ti_le_sai": round(len(wrong) / n, 3),
            "dap_an_sai_nhieu_nhat": top,
            "so_chon_dap_an_do": top_n,
            "sai_co_dap_an": sum(opts.values()),
            "sai_co_lam_lai": sum(1 for a in wrong if (a["hv"], ref) in retried),
            "du_mau": "co" if n >= MIN_N else "chua_du_du_lieu",
        })
    rows.sort(key=lambda r: (r["lesson_id"], r["ref"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    tot_wrong = sum(r["sai_lan_dau"] for r in rows)
    enough = [r for r in rows if r["du_mau"] == "co"]
    print("Lượt trả lời lần đầu bài ôn: %d · sai %d (%.1f%%)" % (len(first), tot_wrong, 100 * tot_wrong / len(first)))
    print("Học viên có làm bài ôn: %d" % len({a["hv"] for a in first}))
    print("Số câu ôn: %d · đủ mẫu (>= %d lượt): %d" % (len(rows), MIN_N, len(enough)))
    ww = sum(r["sai_lan_dau"] for r in rows)
    print("Lượt sai lần đầu có làm lại: %d/%d" % (sum(r["sai_co_lam_lai"] for r in rows), ww))
    conc = [r for r in enough if r["sai_co_dap_an"] >= 5 and r["so_chon_dap_an_do"] / r["sai_co_dap_an"] >= 0.5]
    hi = [r for r in enough if r["ti_le_sai"] >= 0.3]
    print("Câu đủ mẫu có tỉ lệ sai >= 30%%: %d/%d" % (len(hi), len(enough)))
    print("Câu đủ mẫu mà >= 50%% lượt sai dồn vào 1 đáp án (>= 5 lượt sai): %d/%d" % (len(conc), len(enough)))
    print("\nTop 10 câu đủ mẫu theo tỉ lệ sai:")
    for r in sorted(enough, key=lambda r: -r["ti_le_sai"])[:10]:
        print("  %-45s %3d/%-3d (%4.1f%%) · sai chọn %s: %d/%d" % (
            r["ref"], r["sai_lan_dau"], r["n_lan_dau"], 100 * r["ti_le_sai"],
            r["dap_an_sai_nhieu_nhat"] or "-", r["so_chon_dap_an_do"], r["sai_co_dap_an"]))
    print("\nĐã ghi %s (%d câu)" % (os.path.relpath(OUT), len(rows)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
