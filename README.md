# beidou-jb

面向中文小说与电影、剧集、短剧、AI 漫剧、舞台剧的原创、续写、改编、诊断、公平评分和升级 Skill。

## 能力

- 从零创作长篇小说、网文和短篇小说
- 写大纲、卷纲、章节细纲、正文与续写
- 从零创作电影、剧集、竖屏短剧、AI 漫剧和舞台剧剧本
- 检查、修改、重写和升级已有剧本
- 把小说、网文和故事梗概改编为可拍、可演的剧本
- 检查人物动机、因果、信息权限、节奏、高潮、伏笔和连续性
- 按媒介、文本阶段和证据覆盖率评分；缺失维度记为 N/A，不凭空给分
- 优化对白、叙述声音和自然中文表达

Skill 以用户授权、事实连续性、人物选择和因果链为共同底盘。小说与剧本使用不同的正文协议：小说保留 POV、内心和叙述声音；剧本强调可见、可演和体例格式。

## 使用示例

### 小说原创

```text
使用 $beidou-jb 设计一部长篇都市悬疑小说，先给总纲和前三章细纲，不要写正文。
```

```text
使用 $beidou-jb 根据现有设定续写第12章，保持第三人称限知和人物声线，直接给完整正文。
```

### 原创剧本

```text
使用 $beidou-jb 写一集90秒竖屏悬疑短剧，直接给可拍的完整剧本。
```

### 剧本检查与升级

```text
使用 $beidou-jb 检查这份剧本。只列问题、证据和最小修复方案，不要改写。
```

```text
使用 $beidou-jb 修改并升级这份剧本，最后直接给完整终稿。
```

```text
使用 $beidou-jb 给这份舞台剧单场评分。只评价当前材料能证明的维度，报告证据覆盖率和置信度，不要改写。
```

### 小说改编

```text
使用 $beidou-jb 把这篇小说改成竖屏 AI 漫剧。先做改编总纲和分集节拍，再写前3集完整剧本。
```

## 权限规则

- “检查、分析、评分、建议”不自动重写全文。
- “修改、重写、续写、成稿、直接写”交付对应完整文本。
- 只要大纲时不自动写正文。
- 媒介不明确且会改变正文格式时，先确认是小说还是剧本。

## 内部资料

- `novel-writing.md`：小说原创、章节和续写
- `screenplay-creation.md`：原创影视剧本
- `story-structure-options.md`：条件式结构选择
- `genre-and-originality.md`：类型承诺、对标与反套路
- `revision-and-continuity.md`：修改级联与连续性
- `novel-adaptation.md`：小说到剧本改编
- `story-diagnosis.md`：故事诊断
- `human-writing.md`：小说与剧本的自然中文表达
- `ai-comic-execution.md`：AI 漫剧可执行性
- `script-format.md`：电影、剧集、竖屏短剧、AI 漫剧与舞台剧格式
- `quality-gates.md`：小说、通用剧本、竖屏短剧/AI 漫剧的公平评分协议
- `market-and-compliance.md`：市场、版权与合规

## 辅助检查

较长中文剧本可以运行：

```powershell
python scripts/audit_script.py <剧本文件>
```

脚本仅检查中文影视、剧集和竖屏剧本的机械信号，不适用于小说或舞台剧，也不能代替故事判断。可运行回归测试：

```powershell
python -m unittest discover -s tests -v
```

## 说明

内部 S 级或其他评分只表示通过当前媒介量表、文本范围和证据覆盖条件，不代表第三方平台评级、审核结果或商业成功。证据覆盖率低于 60% 时不提供总分和等级。

## 方法来源

本版在原有 `beidou-jb` 基础上，提炼并重新组织了以下开源项目的方法：

- [Oh Story](https://github.com/zenstory-ai/oh-story-claudecode)（MIT）：小说流程、情绪承诺、长篇状态与连续性思路。
- [Screenwriting Skills](https://github.com/jtydhr88/screenwriting-skills)（MIT）：剧本开发阶段、媒介差异和条件式结构选择。
- [jwynia/agent-skills](https://github.com/jwynia/agent-skills)（相关 Skills 标注 MIT）：诊断状态、探索/交付初稿、原创性四轴、场景节奏和修改级联。

融合版只吸收抽象方法与流程，不收录第三方书籍、剧本案例或受保护原文。
