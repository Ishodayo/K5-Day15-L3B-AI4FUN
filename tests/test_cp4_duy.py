import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))
import agent
import tools


class SyntheticTest(unittest.TestCase):
    def setUp(self):
        self.ref = "d05-on-cot-canvas"
        self.card = tools.danh_gia_cau(tools.lay_tin_hieu_cau(self.ref))

    def test_synthetic_does_not_explain_real_responses(self):
        reply = (f"[{self.ref}] Loại: câu hỏi gây nhầm\n"
                 "Vì sao: học viên hiểu sai và đề gốc có lỗi.\n"
                 "Gợi ý: Giải thích canvas. Quiz ví dụ: Bắt đầu từ đâu?")
        with patch.object(agent, "call_model", return_value={"text": reply}) as model:
            result, note = agent._dien_giai([self.card], [])
        data = json.loads(model.call_args.args[1].split("\n", 1)[1])[0]
        self.assertTrue(data["câu hỏi ví dụ"])
        self.assertNotIn("12/12", json.dumps(data, ensure_ascii=False))
        self.assertIn("Loại: cần xem thêm", result)
        self.assertNotIn("học viên hiểu sai", result)
        self.assertIn("Quiz ví dụ", result)
        self.assertFalse(note)

    def test_rejects_suspect_suggestion_and_bad_format(self):
        for output in (f"[{self.ref}] Loại: cần xem thêm\nGợi ý: Học viên hiểu sai.",
                       "Không theo định dạng"):
            with self.subTest(output=output), patch.object(agent, "call_model", return_value={"text": output}):
                result, note = agent._dien_giai([self.card], [])
                self.assertFalse(result)
                self.assertIn("Đã bỏ", note)

    def test_card_marks_concentration_without_kc(self):
        card = agent._the_cau(self.card)
        self.assertIn("Có khả năng câu hỏi gây nhầm", card)
        self.assertNotIn("KC ", card)


if __name__ == "__main__":
    unittest.main()
