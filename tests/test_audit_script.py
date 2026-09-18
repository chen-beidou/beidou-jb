import unittest

from scripts.audit_script import audit, extract_dialogue


class AuditScriptTests(unittest.TestCase):
    def test_metadata_is_not_dialogue(self):
        text = """剧名：雨夜
题材：悬疑
画幅：9:16
单集时长：90秒
本集核心冲突：女儿必须在母亲发现离婚协议前拿回文件

第1集 雨停之前
1-1 饭厅 内 夜
出场：母亲、女儿
△ 母亲低头拣豆。
女儿：明天会下雨吗？
母亲：不会了。
"""
        report = audit(text)
        self.assertEqual(report["dialogue_lines"], 2)
        self.assertEqual(report["speakers"], {"女儿": 1, "母亲": 1})

    def test_long_metadata_does_not_trigger_long_dialogue(self):
        text = "本集核心冲突：" + "这是一段项目说明" * 20
        report = audit(text)
        self.assertFalse(any(item["type"] == "long_dialogue" for item in report["findings"]))

    def test_both_scene_header_styles_are_detected(self):
        vertical = audit("第1集\n1-1 饭厅 内 夜\n甲：走。")
        film = audit("1. 内景 饭厅 — 夜\n甲：走。")
        self.assertEqual(vertical["scene_markers"], 1)
        self.assertEqual(film["scene_markers"], 1)

    def test_real_long_dialogue_is_flagged(self):
        text = "1-1 饭厅 内 夜\n甲：" + "我必须把这件事完整解释清楚" * 10
        report = audit(text)
        findings = [item for item in report["findings"] if item["type"] == "long_dialogue"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["speaker"], "甲")

    def test_mechanical_signals_remain_detectable(self):
        text = """第1集
甲：当然可以，下面是我的回答。😀
**所有人都惊呆了**
未完待续
"""
        report = audit(text)
        types = {item["type"] for item in report["findings"]}
        self.assertTrue({"ai_phrase", "markdown_bold", "emoji", "missing_scene_headers", "weak_ending"}.issubset(types))

    def test_extract_dialogue_accepts_latin_or_middle_dot_names(self):
        dialogue = extract_dialogue("ALEX：Wait.\n阿里·木：别动。")
        self.assertEqual(dialogue, [("ALEX", "Wait."), ("阿里·木", "别动。")])


if __name__ == "__main__":
    unittest.main()
