"""Gọi agent và theo dõi token an toàn giữa các phiên Streamlit."""
import csv
import re
import threading
from pathlib import Path

import tracing
from agent import answer

# tracing.py của khung lưu trạng thái toàn cục. Chỉ chạy một lượt tại một thời điểm
# để các phiên trình duyệt không ghi đè trace và token của nhau.
_lock = threading.Lock()
_LESSON_MAPPING = Path(__file__).resolve().parent.parent / "data" / "lesson_mapping.csv"
_QUESTION_BANK = Path(__file__).resolve().parent.parent / "data" / "question_bank.csv"
_DISPLAY_ID = re.compile(r"\b(?:program-day\d{2}:[a-z0-9-]+(?::(?:module-\d+|lab-[a-z0-9-]+))?|d\d{2}-on-[a-z0-9-]+)\b")


def display_lesson_names(text, mapping_path=None, question_path=None):
    """Đổi nhãn khi hiển thị; không coi câu hỏi synthetic là đề gốc."""
    names = {}
    questions = {}
    try:
        with open(mapping_path or _LESSON_MAPPING, encoding="utf-8-sig", newline="") as f:
            names = {row["lesson_id"]: row["preclass_title"].strip()
                     for row in csv.DictReader(f) if row.get("lesson_id") and row.get("preclass_title")}
    except (OSError, UnicodeError, csv.Error):
        pass
    try:
        with open(question_path or _QUESTION_BANK, encoding="utf-8-sig", newline="") as f:
            questions = {row["ref"]: row for row in csv.DictReader(f)
                         if row.get("ref") and (row.get("de") or "").strip()}
    except (OSError, UnicodeError, csv.Error):
        pass

    def replace(match):
        code = match.group(0)
        question = questions.get(code)
        if question:
            label = "Câu hỏi ví dụ tự soạn, không phải đề gốc" if "synthetic" in question.get("nguon", "").lower() else "Câu hỏi"
            return "%s: %s" % (label, question["de"].strip())
        lesson, separator, part = code.rpartition(":")
        if not separator or not (part.startswith("module-") or part.startswith("lab-")):
            lesson, part = code, ""
        title = names.get(lesson)
        if not title:
            return code
        if part.startswith("module-"):
            return "%s — Phần %s" % (title, part[len("module-"):])
        return "%s — %s" % (title, part) if part else title

    return _DISPLAY_ID.sub(replace, text)


def generate_card(question):
    with _lock:
        tracing.begin("app")
        try:
            result = answer(question)
        finally:
            summary, _ = tracing.end()
        return result.get("output", ""), summary
