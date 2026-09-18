#!/usr/bin/env python3
"""Mechanical screenplay audit. It flags signals; it does not grade story quality."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


AI_PHRASES = [
    "当然可以", "下面是", "希望对你有帮助", "值得注意的是", "综上所述",
    "归根结底", "这不仅仅是", "这不仅是", "真正的", "命运的齿轮",
    "殊不知", "然而他不知道", "然而她不知道", "空气仿佛凝固",
    "这一刻他终于明白", "这一刻她终于明白", "未来可期",
]

WEAK_ENDINGS = ["未完待续", "欲知后事", "他震惊了", "她震惊了", "所有人都惊呆了"]
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF]")
EPISODE_RE = re.compile(r"(?m)^\s*第\s*\d+\s*集")
SCENE_RE = re.compile(
    r"(?m)^\s*(?:\d+[-－—]\d+|\d+[.．、]?)\s+"
    r"(?:(?:内景|外景)\s+.+|.+\s+(?:内|外))"
    r".*(?:日|夜|晨|昏|黎明|黄昏)\s*$"
)
DIALOGUE_RE = re.compile(r"(?m)^\s*([\u4e00-\u9fffA-Za-z·]{1,12})\s*[：:]\s*(.+)$")

METADATA_LABELS = {
    "剧名", "片名", "题材", "类型", "画幅", "时长", "预计时长", "单集时长",
    "集名", "本集核心冲突", "本集情绪兑现", "核心冲突", "情绪兑现",
    "出场", "人物", "地点", "时间", "场景", "幕", "场", "备注", "说明",
}


def extract_dialogue(text: str) -> list[tuple[str, str]]:
    """Return likely dialogue while excluding project and scene metadata."""
    dialogue: list[tuple[str, str]] = []
    for speaker, line in DIALOGUE_RE.findall(text):
        speaker = speaker.strip()
        line = line.strip()
        if speaker in METADATA_LABELS or not line:
            continue
        dialogue.append((speaker, line))
    return dialogue


def audit(text: str) -> dict:
    findings: list[dict] = []

    for phrase in AI_PHRASES:
        count = text.count(phrase)
        if count:
            findings.append({"severity": "warning", "type": "ai_phrase", "match": phrase, "count": count})

    bold_count = text.count("**") // 2
    if bold_count:
        findings.append({"severity": "warning", "type": "markdown_bold", "count": bold_count})

    emoji_count = len(EMOJI_RE.findall(text))
    if emoji_count:
        findings.append({"severity": "warning", "type": "emoji", "count": emoji_count})

    episodes = len(EPISODE_RE.findall(text))
    scenes = len(SCENE_RE.findall(text))
    if scenes == 0:
        findings.append({"severity": "warning", "type": "missing_scene_headers", "count": 1})

    dialogue = extract_dialogue(text)
    long_dialogue = [(speaker, line.strip()) for speaker, line in dialogue if len(line.strip()) > 80]
    for speaker, line in long_dialogue[:10]:
        findings.append({
            "severity": "warning",
            "type": "long_dialogue",
            "speaker": speaker,
            "length": len(line),
            "sample": line[:60],
        })

    stripped = text.rstrip()
    for ending in WEAK_ENDINGS:
        if stripped.endswith(ending) or stripped.endswith(ending + "。"):
            findings.append({"severity": "warning", "type": "weak_ending", "match": ending, "count": 1})

    speakers: dict[str, int] = {}
    for speaker, _ in dialogue:
        speakers[speaker] = speakers.get(speaker, 0) + 1

    return {
        "characters": len(text),
        "episode_markers": episodes,
        "scene_markers": scenes,
        "dialogue_lines": len(dialogue),
        "speakers": speakers,
        "finding_count": len(findings),
        "findings": findings,
        "note": "Mechanical signals only. Review every finding in context; zero findings does not mean the story passes.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a Chinese screenplay for mechanical formatting and AI-style signals.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a readable report.")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8-sig")
    report = audit(text)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"Characters: {report['characters']}")
    print(f"Episode markers: {report['episode_markers']}")
    print(f"Scene markers: {report['scene_markers']}")
    print(f"Dialogue lines: {report['dialogue_lines']}")
    print(f"Findings: {report['finding_count']}")
    for item in report["findings"]:
        details = ", ".join(f"{k}={v}" for k, v in item.items() if k not in {"severity", "type"})
        print(f"- {item['type']}: {details}")
    print(report["note"])


if __name__ == "__main__":
    main()
