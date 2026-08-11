#!/usr/bin/env python3
"""Removes mechanical artifacts left in Markdown by editors and assistants.

Two classes are handled differently, because only one is unambiguously wrong:

- **Fixed:** smart quotes inside code spans. Code shown with curly quotes does not run when
  copied, so `"..."` is restored to `"..."` inside backticks only. Prose keeps its typography.
- **Fixed:** zero-width and formatting characters (ZWSP, BOM, word joiner, invisible separator,
  bidi marks) that carry no meaning in our documents and survive copy-paste invisibly.
- **Fixed:** the deprecated bidi embeddings and overrides (LRE, RLE, PDF, LRO, RLO). They change
  the order a line renders in without changing the characters it contains, so the rendered text and
  the source can read differently. Unicode deprecates them in favour of the isolates reported below.
- **Fixed:** stray Unicode tag characters, which have no rendering of their own.
  Tag characters are **kept** where they form an emoji tag sequence — a waving black flag followed
  by tag letters and a cancel tag, which is how the subdivision flags are written. Stripping those
  would turn a Scotland flag into a plain black one, so the sequence is preserved verbatim.

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

The bidi isolates (LRI, RLI, FSI, PDI) and the Arabic letter mark are **reported, never rewritten**.
They are the current, non-deprecated way to embed a right-to-left run, so a quoted Arabic or Hebrew
example may legitimately carry one — but nothing about the surrounding characters makes one
expected here, so they are always reported rather than suppressed by context.

Variation selectors are **left alone entirely**. U+FE0F is what makes a bare codepoint render as an
emoji rather than a glyph, so removing it silently changes what a reader sees.

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

# Carry no meaning here and are invisible in review, so they are removed outright. Written as
# escapes rather than literals: a table of invisible characters is unreviewable in its own source.
# The bidi embeddings and overrides are deprecated by Unicode: they change the order a line renders
# in without changing the characters it contains, so the same bytes can read two different ways.
STRIP = {"\u200b": "ZWSP", "\ufeff": "BOM", "\u2060": "WORD JOINER",
         "\u2063": "INVISIBLE SEPARATOR", "\u200e": "LTR MARK", "\u200f": "RTL MARK",
         "\u202a": "LRE", "\u202b": "RLE", "\u202c": "PDF",
         "\u202d": "LRO", "\u202e": "RLO"}
# Legitimate typography, so these are never rewritten. They are only reported where a non-breaking
# space makes no sense — between two ordinary words — which is the shape an accidental paste takes.
REPORT = {"\u202f": "NARROW NO-BREAK SPACE", "\u2009": "THIN SPACE",
          "\u200d": "ZWJ", "\u200c": "ZWNJ", "\u00ad": "SOFT HYPHEN"}
# The supported, non-deprecated way to isolate a right-to-left run, so a quoted Arabic or Hebrew
# example may carry one. Unlike REPORT there is no context that makes one expected, so these are
# always reported rather than suppressed by their neighbours.
REPORT_BIDI = {"\u2066": "LRI", "\u2067": "RLI", "\u2068": "FSI", "\u2069": "PDI",
               "\u061c": "ARABIC LETTER MARK"}
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
# A tag sequence is a waving black flag, one or more tag letters, then the cancel tag. That is how
# the subdivision flags are encoded, so the tag block cannot simply be stripped wholesale.
TAG_FIRST, TAG_LAST, TAG_CANCEL = 0xE0000, 0xE007F, "\U000E007F"
TAG_LETTER_FIRST, TAG_LETTER_LAST = 0xE0020, 0xE007E
BLACK_FLAG = "\U0001F3F4"


def is_pictographic(ch):
    """Reports whether the character is an emoji or other pictograph."""
    return bool(ch) and (unicodedata.category(ch) == "So" or ord(ch) >= 0x1F000)


def is_tag_char(ch):
    """Reports whether the character is in the Unicode tag block."""
    return TAG_FIRST <= ord(ch) <= TAG_LAST


def strip_tag_chars(line):
    """Returns the line without stray tag characters, keeping emoji tag sequences intact."""
    if not any(is_tag_char(c) for c in line):
        return line

    out, i = [], 0
    while i < len(line):
        if line[i] == BLACK_FLAG:
            end = i + 1
            while end < len(line) and TAG_LETTER_FIRST <= ord(line[end]) <= TAG_LETTER_LAST:
                end += 1
            # Only a well-formed, terminated sequence is a flag; anything else is a stray tag.
            if end > i + 1 and end < len(line) and line[end] == TAG_CANCEL:
                out.append(line[i:end + 1])
                i = end + 1
                continue
        if not is_tag_char(line[i]):
            out.append(line[i])
        i += 1

    return "".join(out)


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

    return strip_tag_chars(line)


def main():
    check = "--check" in sys.argv
    files = sorted(p for p in REPO_ROOT.rglob("*.md")
                   if not SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts))
    changed, notes = [], []

    for path in files:
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError) as err:
            # One unreadable file must not abort the run for the whole repository: this is wired
            # into `make format` and `make lint`, where a traceback would mask every other result.
            print(f"[warn] unreadable: {path} ({err})", file=sys.stderr)
            continue

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

        for ch, label in REPORT_BIDI.items():
            parts = text.split(ch)
            for part in parts[:-1]:
                notes.append(f"{name}: {label} after {part.rsplit(chr(10), 1)[-1][-24:]!r}")

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
