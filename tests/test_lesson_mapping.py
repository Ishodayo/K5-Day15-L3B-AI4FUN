import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "codebase"))
from ui_service import display_lesson_names


class LessonNamesTest(unittest.TestCase):
    def test_module_and_ai_heading_use_lesson_title(self):
        code = "program-day09:evaluation-failure-analysis:module-3"
        output = display_lesson_names(f"- {code}: 13 câu hỏi\n[{code}] Loại: cần xem thêm")
        self.assertEqual(output.count("Đánh giá và phân tích lỗi — Phần 3"), 2)
        self.assertNotIn(code, output)
        self.assertIn("13 câu hỏi", output)

    def test_exact_mapping_and_unmapped_codes(self):
        code = "program-day03:chatbot-to-agentic-agent"
        unknown = "program-day99:unknown:module-3"
        self.assertEqual(display_lesson_names(f"{code} / {unknown}"),
                         f"Từ chatbot đến agentic agent / {unknown}")

    def test_lab_identifier_remains_distinguishable(self):
        code = "program-day01:ai-llm-foundation:lab-d01-lab-ban-la-llm"
        self.assertEqual(display_lesson_names(code), "AI & LLM Foundation — lab-d01-lab-ban-la-llm")

    def test_missing_mapping_preserves_original(self):
        code = "program-day09:evaluation-failure-analysis:module-3"
        self.assertEqual(display_lesson_names(code, "missing-mapping.csv"), code)

    def test_synthetic_question_is_labelled_not_original(self):
        ref = "d01-on-chon-tang-model"
        text = display_lesson_names(f"- {ref}: 8/35\n[{ref}] Loại: cần xem thêm")
        self.assertEqual(text.count("Câu hỏi ví dụ tự soạn, không phải đề gốc"), 2)
        self.assertIn("Khi triển khai tính năng AI", text)
        self.assertIn("8/35", text)
        self.assertNotIn(ref, text)

    def test_unknown_question_keeps_ref(self):
        ref = "d09-on-khoang-tin-cay"
        self.assertEqual(display_lesson_names(ref), ref)


if __name__ == "__main__":
    unittest.main()
