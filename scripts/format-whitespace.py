#!/usr/bin/env python3
"""Normalizes Markdown whitespace across the PhotoPrism documentation.

Collapses runs of blank lines, enforces exactly one trailing newline, and strips trailing
spaces. This drift is invisible in a rendered diff and accumulates when sections are spliced
in by tooling, so it is normalized mechanically rather than caught by eye.

Two trailing spaces are a Markdown hard line break and are preserved.

Note: this does not skip fenced code blocks, so trailing spaces inside them are stripped too.
That is intentional here - the only occurrences found were accidental, in pasted shell
commands and log output.

Usage:
  python3 ./scripts/format-whitespace.py           # rewrite files in place
  python3 ./scripts/format-whitespace.py --check    # report drift, change nothing
"""
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", "node_modules", "venv", "site", "bin", "styles"}


def normalize(text):
    """Returns the text with blank-line runs, trailing spaces, and the final newline fixed."""
    out = []

    for line in text.split("\n"):
        stripped = line.rstrip()
        # Preserve a Markdown hard break: exactly two spaces after visible content.
        out.append(stripped + "  " if line.endswith("  ") and stripped else stripped)

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.rstrip("\n") + "\n" if text.strip() else ""


def main():
    check = "--check" in sys.argv
    files = sorted(p for p in REPO_ROOT.rglob("*.md")
                   if not SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts))
    changed = []

    for path in files:
        text = path.read_text()
        fixed = normalize(text)

        if fixed != text:
            changed.append(str(path.relative_to(REPO_ROOT)))
            if not check:
                path.write_text(fixed)

    if check and changed:
        for name in changed:
            print(f"[ERROR] Whitespace drift: {name}", file=sys.stderr)
        print(f"Whitespace check failed for {len(changed)} of {len(files)} files.", file=sys.stderr)
        return 1

    verb = "would reformat" if check else "reformatted"
    print(f"Whitespace {'check passed' if check else 'formatted'} "
          f"({len(files)} files checked, {len(changed)} {verb}).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
