"""Gọi agent và theo dõi token an toàn giữa các phiên Streamlit."""
import threading

import tracing
from agent import answer

# tracing.py của khung lưu trạng thái toàn cục. Chỉ chạy một lượt tại một thời điểm
# để các phiên trình duyệt không ghi đè trace và token của nhau.
_lock = threading.Lock()


def generate_card(question):
    with _lock:
        tracing.begin("app")
        try:
            result = answer(question)
        finally:
            summary, _ = tracing.end()
        return result.get("output", ""), summary
