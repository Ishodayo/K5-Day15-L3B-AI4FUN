"""Kiểm hợp đồng token và không diễn giải đề tổng hợp như đề gốc."""
import json
import sys
import unittest
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))
import ai
import agent


class ModelTests(unittest.TestCase):
    def test_gemini_retries_rate_limit_after_requested_delay(self):
        error = urllib.error.HTTPError("https://example.invalid", 429, "rate limit", {"Retry-After": "3"}, None)
        response = BytesIO(b'{"ok": true}')
        with patch.object(ai.urllib.request, "urlopen", side_effect=[error, response]) as request, \
             patch.object(ai.time, "sleep") as sleep:
            self.assertEqual(ai._post_json("https://example.invalid", {}, {}, retries=2), {"ok": True})
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(3.0)

    def test_long_retry_after_does_not_block(self):
        error = urllib.error.HTTPError("https://example.invalid", 429, "quota", {"Retry-After": "3600"}, None)
        with patch.object(ai.urllib.request, "urlopen", side_effect=error), patch.object(ai.time, "sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "429"):
                ai._post_json("https://example.invalid", {}, {}, retries=2)
        sleep.assert_not_called()

    def test_gemini_counts_thinking_tokens(self):
        response = {"usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 4,
                                      "thoughtsTokenCount": 7},
                    "candidates": [{"content": {"parts": [{"text": "Đáp án"}]}}]}
        with patch.object(ai, "MODEL_PROVIDER", "gemini"), patch.object(ai, "MODEL_NAME", "test-model"), \
             patch.object(ai, "API_KEY", "test-key"), patch.object(ai, "_post_json", return_value=response):
            self.assertEqual(ai.call_model("system", "user"),
                             {"text": "Đáp án", "model": "test-model", "tokens_in": 12, "tokens_out": 11})

    def test_synthetic_question_not_sent_to_model(self):
        question = {"ref": "d05-on-test", "kc_code": "test", "sai": 10, "n": 15, "ti_le": 10 / 15,
                    "dap_an": "A", "don": 10, "co_da": 10, "nhan": "sai_don_mot_dap_an"}
        synthetic = {"de": "Đề tự soạn", "cac_dap_an": "A. giả", "dap_an_dung": "A", "nguon": "synthetic"}
        with patch.object(agent, "lay_de_cau_hoi", return_value=synthetic), \
             patch.object(agent, "call_model", return_value={"text": "Cần xem đề gốc"}) as model:
            result, warning = agent._dien_giai([question], [])
        cards = json.loads(model.call_args.args[1].split("\n", 1)[1])
        self.assertEqual(cards[0]["de"], "chưa có đề")
        self.assertNotIn("Đề tự soạn", json.dumps(cards, ensure_ascii=False))
        self.assertIn("đề gốc không có", result)
        self.assertFalse(warning)


if __name__ == "__main__":
    unittest.main()
