# 《生土生水》· 五级史诗故事讲述练习集

这是《生土生水》（芒族史诗 *Đẻ đất đẻ nước*）的简体中文版语料库，面向 **9–10 岁**儿童，包含 **6 幕 · 28 章 · 28 幅记忆画作提示 · 5 个练习级别**。

## 五个级别

| 级别 | 目录 | 内容 |
| :--- | :--- | :--- |
| **Level 0** | [level-0-context/](level-0-context/) | 史诗背景、芒族文化、参考古籍与人物地名资料 |
| **Level 1** | [level-1-full-text/](level-1-full-text/) | 28 章朗读文本框架与中文讲述语气提示 |
| **Level 2** | [level-2-detailed-outline/](level-2-detailed-outline/) | 28 章中文详细提纲（人物与意象、详细发展、讲述重点） |
| **Level 3** | [level-3-summary-outline/chapter-summaries.md](level-3-summary-outline/chapter-summaries.md) | 28 章精简总纲 |
| **Level 4** | [level-4-visual-prompts/](level-4-visual-prompts/) | 28 幅纯视觉记忆画作题材与图集目录（画作尚待绘制，`image_generated=false`） |

机器可读索引：[story-index.json](story-index.json)。

## 诚实说明

- Level 0（总览、六幕背景、八篇参考资料）、Level 2、Level 3、Level 4 与 28 章讲述语气提示均已完成简体中文整理。
- Level 1 诗行正文与原始古籍全本正待进一步完整汉译（当前保留对照英译全本以防删漏诗行）。
- 28 幅 Level 4 插图尚待绘制（`image_generated=false`）。

## 数据检查

```bash
python3 scripts/validate_corpus.py --locale zh --draft
```
