import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


class SkillIntegrityTests(unittest.TestCase):
    def test_frontmatter_has_only_supported_keys(self):
        text = SKILL.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0].strip()
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual(keys, {"name", "description"})

    def test_references_named_by_skill_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        targets = set(re.findall(r"references/[A-Za-z0-9._/-]+\.md", text))
        self.assertGreaterEqual(len(targets), 12)
        missing = [target for target in targets if not (ROOT / target).is_file()]
        self.assertEqual(missing, [])

    def test_main_skill_stays_compact(self):
        lines = SKILL.read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 500)

    def test_long_references_have_contents(self):
        missing_contents = []
        for path in (ROOT / "references").glob("*.md"):
            lines = path.read_text(encoding="utf-8").splitlines()
            if len(lines) > 100 and "## 目录" not in lines[:30]:
                missing_contents.append(path.name)
        self.assertEqual(missing_contents, [])

    def test_fair_scoring_guards_are_present(self):
        text = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
        for required in ["N/A", "证据不足", "证据覆盖率", "置信度", "小说量表", "通用剧本量表"]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
