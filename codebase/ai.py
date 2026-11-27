"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example). Hỗ trợ Gemini, OpenAI, Claude và Ollama;
không dán API key vào file này. Xem thêm docs/connect-model.md.
"""
import os
import json
import urllib.error
import urllib.parse
import urllib.request
import time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def _retry_after(headers):
    value = headers.get("Retry-After") if headers else None
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            return max(0.0, (parsedate_to_datetime(value) - datetime.now(timezone.utc)).total_seconds())
        except (TypeError, ValueError, OverflowError):
            return None


def _post_json(url, headers, body, timeout=60, retries=0):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            delay = _retry_after(exc.headers)
            if delay is None:
                delay = 2 ** (attempt + 1)
            # Không thử liên tục hoặc chờ lâu khi quota ngày đã hết.
            if exc.code in (429, 503) and attempt < retries and delay <= 15:
                time.sleep(delay)
                continue
            hint = " Hãy thử lại sau hoặc kiểm tra hạn mức API." if exc.code in (429, 503) else ""
            raise RuntimeError("Gọi model thất bại: HTTP %d.%s" % (exc.code, hint)) from exc


def _messages(system, user):
    return ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user}]


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if not MODEL_NAME:
        raise ValueError("Chưa đặt MODEL_NAME trong .env")
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise ValueError("Chưa đặt API_KEY trong .env")

    if MODEL_PROVIDER == "openai":
        data = _post_json("https://api.openai.com/v1/chat/completions",
                          {"Authorization": "Bearer " + API_KEY},
                          {"model": MODEL_NAME, "messages": _messages(system, user)})
        usage = data["usage"]
        text, tokens_in, tokens_out = (data["choices"][0]["message"]["content"],
                                       usage["prompt_tokens"], usage["completion_tokens"])
    elif MODEL_PROVIDER == "anthropic":
        data = _post_json("https://api.anthropic.com/v1/messages",
                          {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                          {"model": MODEL_NAME, "max_tokens": 4096, "system": system or "",
                           "messages": [{"role": "user", "content": user}]})
        usage = data["usage"]
        text = "".join(part.get("text", "") for part in data["content"] if part.get("type") == "text")
        tokens_in, tokens_out = usage["input_tokens"], usage["output_tokens"]
    elif MODEL_PROVIDER == "ollama":
        data = _post_json("http://localhost:11434/api/chat", {},
                          {"model": MODEL_NAME, "messages": _messages(system, user), "stream": False},
                          timeout=300)
        text, tokens_in, tokens_out = data["message"]["content"], data["prompt_eval_count"], data["eval_count"]
    elif MODEL_PROVIDER == "gemini":
        model = MODEL_NAME[7:] if MODEL_NAME.startswith("models/") else MODEL_NAME
        url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % urllib.parse.quote(model, safe="")
        body = {"contents": [{"role": "user", "parts": [{"text": user}]}]}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        data = _post_json(url, {"x-goog-api-key": API_KEY}, body, timeout=120, retries=2)
        usage = data["usageMetadata"]
        parts = data["candidates"][0]["content"]["parts"]
        text = "".join(part.get("text", "") for part in parts if not part.get("thought"))
        tokens_in = usage["promptTokenCount"]
        tokens_out = usage.get("candidatesTokenCount", 0) + usage.get("thoughtsTokenCount", 0)
    else:
        raise ValueError("MODEL_PROVIDER không được hỗ trợ: %s" % MODEL_PROVIDER)
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Model không trả về nội dung văn bản")
    return {"text": text, "model": MODEL_NAME, "tokens_in": int(tokens_in), "tokens_out": int(tokens_out)}
