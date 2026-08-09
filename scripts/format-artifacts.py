#!/usr/bin/env python3
"""Removes mechanical artifacts left in Markdown by editors and assistants.

Two classes are handled differently, because only one is unambiguously wrong:

- **Fixed:** smart quotes inside code spans. Code shown with curly quotes does not run when
  copied, so `"..."` is restored to `"..."` inside backticks only. Prose keeps its typography.
- **Fixed:** zero-width and formatting characters (ZWSP, BOM, word joiner, invisible separator,
  bidi marks) that carry no meaning in our documents and survive copy-paste invisibly.

Three neighbours of that set are **reported, never rewritten**, because each is load-bearing
somewhere we plausibly write:

- **ZWJ** joins an emoji sequence. Removing it splits the glyph: U+1F468 ZWJ U+1F680 renders as
  the astronaut emoji, and without the joiner it becomes a man and a rocket side by side.
- **ZWNJ** is meaningful in Persian, Urdu and several Indic scripts, where it keeps letters
  from joining.
- **SOFT HYPHEN** marks a hyphenation point inside a word, which is exactly where a real one
  appears, so position cannot tell it apart from a pasted one. German compounds use it
  deliberately.

Narrow no-break and thin spaces are **reported, never rewritten**: they are correct typography
between a number and its unit (`720 px`, `5 MiB`) and appear that way throughout the specs.

- **Fixed:** citation markers from browsing or retrieval tools, which are unambiguous and never
  valid content here.

Bracketed index markers (`[1]`, `[2, 3]`) are deliberately **not** matched. They are the Perplexity
and RAG citation style, but in a technical repository they collide with array indices, tensor
shapes and `jq` expressions — a scan found 40 such uses and no real citations. Matching them would
make the check unusable.

Usage:
  python3 ./scripts/format-artifacts.py            # rewrite files in place
  python3 ./scripts/format-artifacts.py --check    # report, change nothing
"""
import pathlib
import re
import sys
import unicodedata

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", "node_modules", "venv", "site", "bin", "styles"}

# Carry no meaning here and are invisible in review, so they are removed outright.
STRIP = {"​": "ZWSP", "﻿": "BOM", "⁠": "WORD JOINER",
         "⁣": "INVISIBLE SEPARATOR", "‎": "LTR MARK", "‏": "RTL MARK"}
# Legitimate typography, so these are never rewritten. They are only reported where a non-breaking
# space makes no sense — between two ordinary words — which is the shape an accidental paste takes.
REPORT = {" ": "NARROW NO-BREAK SPACE", " ": "THIN SPACE",
          "‍": "ZWJ", "‌": "ZWNJ", "­": "SOFT HYPHEN"}
TYPOGRAPHIC = re.compile(r"(?:[\d.%\u2265\u2264=~\u2260<>+-]|\b[A-Z][\w.‑-]*)\Z")
QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
CODE_SPAN = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
# Citation markers leaked by browsing and retrieval tooling. Each is distinctive enough that a
# match is never legitimate prose; see the module docstring for the patterns left out on purpose.
CITATIONS = re.compile(
    r"【\d+(?::\d+)?†source】"
    r"|\{CITATION_START\}cite\{CITATION_DELIMITER\}[^{}]*(?:\{CITATION_DELIMITER\}[^{}]*)*\{CITATION_STOP\}"
    r"|\[\^\d+\^\]"
    r"|\[\d+\^{3}\s*\]"
    r"|\[Ref\s*\d+\]"
    r"|\(source:\s*\d+\)"
    r"|:contentReference\[[^\]]*\]\{[^}]*\}"
    r"|\boaicite:\d+\b"
)


ZWJ, ZWNJ, SOFT_HYPHEN = "\u200d", "\u200c", "\u00ad"


def is_pictographic(ch):
    """Reports whether the character is an emoji or other pictograph."""
    return bool(ch) and (unicodedata.category(ch) == "So" or ord(ch) >= 0x1F000)


def fix_line(line):
    """Returns the line with code-span quotes straightened, invisibles and citations removed."""
    line = CODE_SPAN.sub(lambda m: "`" + m.group(1).translate(QUOTES) + "`", line)
    # Tidy the gap a removed marker leaves, but only on lines that actually had one —
    # collapsing spaces everywhere would destroy Markdown table alignment.
    stripped = CITATIONS.sub("", line)
    if stripped != line:
        stripped = re.sub(r" +([.,;:!?)])", r"\1", stripped)
        stripped = re.sub(r"(\S) {2,}(\S)", r"\1 \2", stripped)
    line = stripped

    for ch in STRIP:
        line = line.replace(ch, "")

    return line


def main():
    check = "--check" in sys.argv
    files = sorted(p for p in REPO_ROOT.rglob("*.md")
                   if not SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts))
    changed, notes = [], []

    for path in files:
        text = path.read_text()
        name = path.relative_to(REPO_ROOT)
        fixed = "\n".join(fix_line(l) for l in text.split("\n"))

        for ch, label in REPORT.items():
            parts = text.split(ch)
            for i, part in enumerate(parts[:-1]):
                # Correct before a number, a unit, an operator, or a capitalized product name.
                after = parts[i + 1][:1]
                before = part[-1:]
                if (TYPOGRAPHIC.search(part.rsplit("\n", 1)[-1]) or after.isdigit()
                        or after.isupper() or after in "=\u2265\u2264<>\u2260+-\u00d7\u00f7"):
                    continue
                # Suppress the ones sitting where they belong, or the note fires on every run and
                # stops being read. A joiner between two pictographs is an emoji sequence; a ZWNJ
                # or soft hyphen between two letters is doing its job.
                if ch == ZWJ and is_pictographic(before) and is_pictographic(after):
                    continue
                if ch in (ZWNJ, SOFT_HYPHEN) and before.isalpha() and after.isalpha():
                    continue
                notes.append(f"{name}: unexpected {label} after {part.rsplit(chr(10), 1)[-1][-24:]!r}")

        if fixed != text:
            changed.append(str(name))
            if not check:
                path.write_text(fixed)

    for note in notes:
        print(f"[note] {note}")

    if check and changed:
        for name in changed:
            print(f"[ERROR] Artifact drift: {name}", file=sys.stderr)
        print(f"Artifact check failed for {len(changed)} of {len(files)} files.", file=sys.stderr)
        return 1

    print(f"Artifact {'check passed' if check else 'formatted'} "
          f"({len(files)} files checked, {len(changed)} {'would be' if check else ''} fixed).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
