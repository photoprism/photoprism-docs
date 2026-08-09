#!/usr/bin/env python3
"""Reformats Markdown tables without touching fenced code blocks.

`markdown-table-formatter` aligns any run of pipe-delimited lines it finds, and it does not
know about code fences. Sample CLI output is frequently drawn with pipes, so running the
formatter directly rewrites the *documented output of a program* to a shape the program never
prints. This wrapper masks every fenced block behind a sentinel, formats what is left, and
restores the blocks verbatim.

Two tables are also left alone entirely:

- Centre-aligned tables whose rows carry no leading pipe. Padding a centred cell puts spaces
  before the first pipe; past four, Markdown reads the line as an indented code block and the
  table stops rendering. Pass such files via --exclude.

Usage:
  python3 ./scripts/format-tables.py                 # rewrite files in place
  python3 ./scripts/format-tables.py --check         # report drift, change nothing
  python3 ./scripts/format-tables.py --exclude a.md  # skip a path (repeatable)
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".claude", "node_modules", "venv", "site", "bin", "styles"}
FENCE_RE = re.compile(r"\s*(```|~~~)")
SENTINEL = "<!-- fenced-block-{} -->"


def mask_fences(text):
    """Returns the text with each fenced block replaced by a sentinel, plus the blocks."""
    out, blocks, current = [], [], None

    for line in text.split("\n"):
        if FENCE_RE.match(line):
            if current is None:
                current = [line]
            else:
                current.append(line)
                blocks.append("\n".join(current))
                out.append(SENTINEL.format(len(blocks) - 1))
                current = None
            continue
        (current if current is not None else out).append(line)

    # An unterminated fence is malformed Markdown; keep it verbatim rather than guessing.
    if current is not None:
        out.extend(current)

    return "\n".join(out), blocks


def restore_fences(text, blocks):
    """Returns the text with every sentinel replaced by its original block."""
    for i, block in enumerate(blocks):
        text = text.replace(SENTINEL.format(i), block)
    return text


def format_batch(paths, check):
    """Masks fences, formats every file in one npx call, restores, and returns what changed.

    The formatter is invoked once for the whole set rather than per file: npx start-up
    dominates the runtime, so a per-file call turns a two-second job into minutes.
    """
    originals = {p: p.read_text() for p in paths}
    changed = []

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        scratch = {}

        for i, path in enumerate(paths):
            masked, blocks = mask_fences(originals[path])
            # Flat names keep the npx argument list simple; the index keeps them unique.
            target = root / f"{i}.md"
            target.write_text(masked)
            scratch[path] = (target, blocks)

        subprocess.run(["npx", "--yes", "markdown-table-formatter",
                        *[str(t) for t, _ in scratch.values()]],
                       check=True, capture_output=True)

        for path, (target, blocks) in scratch.items():
            formatted = restore_fences(target.read_text(), blocks)
            if formatted != originals[path]:
                changed.append(path)
                if not check:
                    path.write_text(formatted)

    return changed


def main():
    check = "--check" in sys.argv
    excluded = {REPO_ROOT / a for i, a in enumerate(sys.argv)
                if i and sys.argv[i - 1] == "--exclude"}

    if not shutil.which("npx"):
        print("format-tables: npx not found; install Node.js to use this target.", file=sys.stderr)
        return 1

    files = sorted(p for p in REPO_ROOT.rglob("*.md")
                   if not SKIP_DIRS & set(p.relative_to(REPO_ROOT).parts)
                   and p.resolve() not in {e.resolve() for e in excluded if e.exists()})
    changed = [str(p.relative_to(REPO_ROOT)) for p in format_batch(files, check)]

    if check and changed:
        for name in changed:
            print(f"[ERROR] Table drift: {name}", file=sys.stderr)
        print(f"Table check failed for {len(changed)} of {len(files)} files.", file=sys.stderr)
        return 1

    verb = "would reformat" if check else "reformatted"
    print(f"Tables {'check passed' if check else 'formatted'} "
          f"({len(files)} files checked, {len(changed)} {verb}).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
