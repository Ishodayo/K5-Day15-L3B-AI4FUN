"""Kiểm tra luồng nhập và trình bày thẻ của giao diện Streamlit."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "codebase"))
import ui_service


class StreamlitUITests(unittest.TestCase):
    def test_example_submission_displays_card_and_usage(self):
        app = AppTest.from_file(str(ROOT / "codebase" / "ui.py")).run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertEqual(app.text_area[0].value, "Ngày 5 lớp vướng gì?")
        summary = {"models": ["test-model"], "tokens_in": 12, "tokens_out": 5}
        with patch.object(ui_service, "generate_card", return_value=("THẺ ĐIỂM NGHẼN\nD. Diễn giải\nGợi ý", summary)) as generate:
            app.button[1].click().run()
        generate.assert_called_once_with("Ngày 5 lớp vướng gì?")
        self.assertFalse(app.exception)
        self.assertTrue(any("test-model" in caption.value and "12" in caption.value for caption in app.caption))
        self.assertTrue(any("D. Diễn giải" in item.value for item in app.markdown))

    def test_error_is_visible(self):
        app = AppTest.from_file(str(ROOT / "codebase" / "ui.py")).run()
        app.text_area[0].input("Ngày 5 lớp vướng gì?")
        with patch.object(ui_service, "generate_card", side_effect=RuntimeError("HTTP 429")):
            app.button[1].click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("429" in message.value for message in app.error))


if __name__ == "__main__":
    unittest.main()
