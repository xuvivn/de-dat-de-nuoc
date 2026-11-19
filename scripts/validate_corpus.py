#!/usr/bin/env python3
"""Kiểm tra tính nhất quán của kho sử thi Đẻ Đất Đẻ Nước.

Cách dùng:
    python3 scripts/validate_corpus.py --draft   # cho phép thiếu tệp đang biên soạn
    python3 scripts/validate_corpus.py           # yêu cầu đầy đủ 28/28 chương, 28/28 ảnh
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "locales" / "vi" / "story-index.json"

CHAPTER_HEADING = re.compile(r"^###\s+Chương\s+(\d+)\s*[:：]\s*(.+?)\s*$")
BOOK_HEADING = re.compile(r"^##\s+(?:Hồi|Quyển)\s+([IVX]+)\b[^\n]*$")
LEVEL0_SECTION = re.compile(r"^##\s+([1-5])\.\s*(.+?)\s*$", re.MULTILINE)
MARKDOWN_MARKERS = ("#", "-", "*", ">", "|", "!", "`", "---")
PLACEHOLDERS = ("TODO", "TBD", "FIXME", "Lorem ipsum", "XXX")

WORD_MIN = 300
WORD_MAX = 3000
VERSE_MAX_WORDS = 14


class Report:
    def __init__(self, draft: bool) -> None:
        self.draft = draft
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def missing(self, message: str) -> None:
        if self.draft:
            self.warn(message)
        else:
            self.error(message)

    def ok(self) -> bool:
        return not self.errors

    def emit(self) -> None:
        for note in self.notes:
            print(f"  · {note}")
        for warning in self.warnings:
            print(f"  ! {warning}")
        for error in self.errors:
            print(f"  x {error}")
        print()
        if self.errors:
            print(f"KẾT QUẢ: {len(self.errors)} lỗi, {len(self.warnings)} cảnh báo")
        else:
            print(f"KẾT QUẢ: đạt ({len(self.warnings)} cảnh báo)")


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path, report: Report) -> str | None:
    if not path.exists():
        report.missing(f"Thiếu tệp: {relative(path)}")
        return None
    return path.read_text(encoding="utf-8")


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-–—]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)
    return text


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", strip_markdown(text)))


def parse_chapters(markdown: str) -> list[dict]:
    lines = markdown.replace("\r\n", "\n").split("\n")
    chapters: list[dict] = []
    current: dict | None = None
    for line in lines:
        match = CHAPTER_HEADING.match(line)
        if match:
            if current:
                chapters.append(current)
            current = {
                "number": int(match.group(1)),
                "title": match.group(2).strip(),
                "lines": [],
            }
            continue
        if current is not None:
            if line.startswith("## ") and not line.startswith("### "):
                chapters.append(current)
                current = None
                continue
            current["lines"].append(line)
    if current:
        chapters.append(current)
    for chapter in chapters:
        chapter["body"] = "\n".join(chapter.pop("lines"))
    return chapters


def check_verse_lines(markdown: str, label: str, report: Report) -> list[int]:
    long_lines: list[int] = []
    in_body = False
    for line in markdown.replace("\r\n", "\n").split("\n"):
        if line.startswith("#### Lưu ý giọng kể"):
            in_body = False
        if CHAPTER_HEADING.match(line):
            in_body = True
            continue
        if not in_body:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith(MARKDOWN_MARKERS):
            continue
        words = len(stripped.split())
        if words > VERSE_MAX_WORDS:
            long_lines.append(words)
    if long_lines:
        report.warn(
            f"{label}: {len(long_lines)} dòng thơ dài hơn {VERSE_MAX_WORDS} chữ "
            f"(dài nhất {max(long_lines)} chữ)"
        )
    return long_lines


def check_level1_book(path: Path, expected: dict[int, str], report: Report) -> None:
    text = read_text(path, report)
    if text is None:
        return
    chapters = parse_chapters(text)
    seen = set()
    for chapter in chapters:
        number = chapter["number"]
        seen.add(number)
        title = expected.get(number)
        if title is None:
            report.error(f"{relative(path)}: chương {number} không có trong story-index")
            continue
        if chapter["title"] != title:
            report.error(
                f"{relative(path)}: tiêu đề chương {number} lệch index\n"
                f"    file:  {chapter['title']}\n"
                f"    index: {title}"
            )
        words = count_words(chapter["body"])
        if words == 0:
            report.error(f"{relative(path)}: chương {number} rỗng")
        elif not (WORD_MIN <= words <= WORD_MAX):
            report.warn(
                f"{relative(path)}: chương {number} có {words} chữ "
                f"(khuyến nghị {WORD_MIN}–{WORD_MAX})"
            )
    missing = sorted(set(expected) - seen)
    if missing:
        report.missing(f"{relative(path)}: thiếu chương {missing}")
    check_verse_lines(text, relative(path), report)


def check_level2_book(path: Path, expected: dict[int, str], report: Report) -> None:
    text = read_text(path, report)
    if text is None:
        return
    chapters = parse_chapters(text)
    seen = set()
    for chapter in chapters:
        number = chapter["number"]
        seen.add(number)
        title = expected.get(number)
        if title is None:
            report.error(f"{relative(path)}: chương {number} không có trong story-index")
            continue
        if chapter["title"] != title:
            report.error(
                f"{relative(path)}: tiêu đề chương {number} lệch index\n"
                f"    file:  {chapter['title']}\n"
                f"    index: {title}"
            )
        body = chapter["body"]
        for label in ("Nhân vật", "Diễn biến", "Ý nghĩa"):
            if label.lower() not in body.lower():
                report.warn(f"{relative(path)}: chương {number} thiếu khối “{label}”")
    missing = sorted(set(expected) - seen)
    if missing:
        report.missing(f"{relative(path)}: thiếu chương {missing}")


def check_level3(path: Path, chapters: list[dict], report: Report) -> None:
    text = read_text(path, report)
    if text is None:
        return
    current_book = ""
    seen: list[tuple[str, int, str]] = []
    for line in text.replace("\r\n", "\n").split("\n"):
        book = BOOK_HEADING.match(line)
        if book:
            current_book = book.group(1)
            continue
        heading = CHAPTER_HEADING.match(line)
        if heading:
            seen.append((current_book, int(heading.group(1)), heading.group(2).strip()))

    expected = {(ch["section"], ch["chapter_number"], ch["title"]) for ch in chapters}
    if len(seen) != len(chapters):
        report.missing(
            f"{relative(path)}: có {len(seen)} chương, cần {len(chapters)}"
        )
    seen_numbers = {number for _, number, _ in seen}
    expected_numbers = {ch["chapter_number"] for ch in chapters}
    missing = sorted(expected_numbers - seen_numbers)
    if missing:
        report.missing(f"{relative(path)}: thiếu chương {missing}")
    for _, number, title in seen:
        match = next((ch for ch in chapters if ch["chapter_number"] == number), None)
        if match and match["title"] != title:
            report.error(
                f"{relative(path)}: tiêu đề chương {number} lệch index\n"
                f"    file:  {title}\n"
                f"    index: {match['title']}"
            )
    _ = expected


def check_level0_overview(path: Path, report: Report) -> None:
    text = read_text(path, report)
    if text is None:
        return
    sections = LEVEL0_SECTION.findall(text)
    if len(sections) != 5:
        report.warn(
            f"{relative(path)}: có {len(sections)} mục cấp 2 dạng “N. …”, "
            "khuôn mẫu cần 5 mục"
        )


def check_images(illustrations: list[dict], report: Report) -> None:
    """Chỉ bắt lỗi với tranh đã đánh dấu image_generated.

    Level 4 hiện dừng ở bộ đề bài vẽ; 28 tranh có thể được tạo sau mà không
    làm hỏng tính nhất quán của kho dữ liệu.
    """
    generated = [ill for ill in illustrations if ill.get("image_generated")]
    pending = [ill for ill in illustrations if not ill.get("image_generated")]

    missing = [ROOT / ill["image"] for ill in generated if not (ROOT / ill["image"]).exists()]
    if missing:
        report.error(
            f"Thiếu {len(missing)}/{len(generated)} tranh đã đánh dấu image_generated: "
            f"{[relative(p) for p in missing[:3]]}"
        )

    small = [
        ROOT / ill["image"]
        for ill in generated
        if (ROOT / ill["image"]).exists() and (ROOT / ill["image"]).stat().st_size < 10_000
    ]
    if small:
        report.warn(f"{len(small)} tranh nhỏ hơn 10 KB: {[relative(p) for p in small[:3]]}")

    if pending:
        report.note(
            f"{len(pending)}/{len(illustrations)} tranh chưa tạo "
            "(image_generated=false) — Level 4 hiện là bộ đề bài vẽ"
        )


def find_placeholders(path: Path, report: Report) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for token in PLACEHOLDERS:
        if token in text:
            report.error(f"{relative(path)}: còn giữ chỗ “{token}”")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", action="store_true", help="cho phép thiếu tệp đang biên soạn")
    args = parser.parse_args()
    report = Report(draft=args.draft)

    if not INDEX_PATH.exists():
        print(f"x Không tìm thấy {relative(INDEX_PATH)}")
        return 1

    try:
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"x JSON không hợp lệ trong {relative(INDEX_PATH)}: {exc}")
        return 1

    chapters = index.get("chapters", [])
    books = index.get("books", [])
    illustrations = index.get("illustrations", [])

    if index.get("total_chapters") != len(chapters):
        report.error(
            f"total_chapters={index.get('total_chapters')} nhưng có {len(chapters)} chương"
        )
    if index.get("total_books") != len(books):
        report.error(f"total_books={index.get('total_books')} nhưng có {len(books)} Hồi")
    if index.get("total_illustrations") != len(illustrations):
        report.error(
            f"total_illustrations={index.get('total_illustrations')} "
            f"nhưng có {len(illustrations)} tranh"
        )

    ids = [ch.get("id") for ch in chapters]
    if len(ids) != len(set(ids)):
        report.error("Có id chương trùng lặp trong story-index")
    numbers = [ch.get("global_number") for ch in chapters]
    if numbers != list(range(1, len(chapters) + 1)):
        report.error("global_number phải liên tục từ 1 đến 28")

    book_ids = {b.get("id") for b in books}
    for ch in chapters:
        if ch.get("book_id") not in book_ids:
            report.error(f"{ch.get('id')}: book_id không tồn tại ({ch.get('book_id')})")
        if ch.get("chapter_number") != ch.get("global_number"):
            report.warn(
                f"{ch.get('id')}: chapter_number khác global_number "
                f"({ch.get('chapter_number')} ≠ {ch.get('global_number')})"
            )

    title_by_book: dict[str, dict[int, str]] = {bid: {} for bid in book_ids}
    for ch in chapters:
        title_by_book.setdefault(ch["book_id"], {})[ch["chapter_number"]] = ch["title"]

    # Level 1
    for book in books:
        path = ROOT / "locales" / "vi" / book["level_1_file"]
        check_level1_book(path, title_by_book[book["id"]], report)

    # Level 2
    for book in books:
        path = ROOT / "locales" / "vi" / book["level_2_file"]
        check_level2_book(path, title_by_book[book["id"]], report)

    # Level 3
    check_level3(ROOT / "locales" / "vi" / "level-3-summary-outline" / "chapter-summaries.md", chapters, report)

    # Level 0
    level0 = index.get("levels", [{}])[0]
    if level0.get("overview_file"):
        check_level0_overview(ROOT / "locales" / "vi" / level0["overview_file"], report)
    for book in books:
        check_level0_overview(ROOT / "locales" / "vi" / book["level_0_file"], report)
    source_text = index.get("source_text")
    if source_text:
        source_path = ROOT / "locales" / "vi" / source_text
        read_text(source_path, report)
        root_source = ROOT / "Đẻ đất đẻ nước.md"
        if root_source.exists():
            report.error("Không được giữ bản sao chính văn trùng lặp tại thư mục gốc: " + relative(root_source))
        ancient_files = {ancient.get("file") for ancient in level0.get("ancient_books", [])}
        if source_text not in ancient_files:
            report.error("source_text chưa được đăng ký trong ancient_books của Level 0")
    for ancient in level0.get("ancient_books", []):
        path = ROOT / "locales" / "vi" / ancient["file"]
        read_text(path, report)

    # Level 4
    check_images(illustrations, report)
    level4 = index.get("levels", [{}, {}, {}, {}, {}])[4]
    for key in ("gallery_file", "prompt_spec_file"):
        if level4.get(key):
            read_text(ROOT / "locales" / "vi" / level4[key], report)

    # Placeholders trong các tệp đã có
    for path in (ROOT / "locales" / "vi").rglob("*.md"):
        find_placeholders(path, report)

    print("=== Đẻ Đất Đẻ Nước · kiểm tra kho dữ liệu ===")
    print(f"Chế độ: {'draft' if args.draft else 'đầy đủ'}")
    print(f"Hồi: {len(books)} · Chương: {len(chapters)} · Tranh: {len(illustrations)}")
    print()
    report.emit()
    return 0 if report.ok() else 1


if __name__ == "__main__":
    sys.exit(main())
