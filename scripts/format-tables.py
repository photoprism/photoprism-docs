#!/usr/bin/env python3
"""Reformats Markdown tables without touching fenced code blocks.

`markdown-table-formatter` aligns any run of pipe-delimited lines it finds, and it does not
know about code fences. Sample CLI output is frequently drawn with pipes, so running the
formatter directly rewrites the *documented output of a program* to a shape the program never
prints. This wrapper masks every fenced block behind a sentinel, formats what is left, and
restores the blocks verbatim.

Every table row needs a leading pipe. Padding a centered cell puts spaces before the first
pipe; past four, Markdown reads the line as an indented code block and the table stops
rendering. Give such a table its leading pipes rather than excluding the file, so it stays
aligned like every other one; --exclude is for a table that must keep a shape this formatter
would otherwise change.

Usage:
  python3 ./scripts/format-tables.py                 # rewrite every Markdown file
  python3 ./scripts/format-tables.py --check         # report drift, change nothing
  python3 ./scripts/format-tables.py --exclude a.md  # skip a path (repeatable)
  python3 ./scripts/format-tables.py a.md dir/       # format the named files and directories
  python3 ./scripts/format-tables.py --all           # include the dated records a sweep keeps
  python3 ./scripts/format-tables.py --help          # print this text, change nothing
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

# Dated records filed under a year are kept as written rather than swept, as are the indexes and
# ledgers beside them. Aligning a table changes no word, so reports are swept like any other file;
# a repository that keeps no such records leaves this empty.
SKIP_PREFIXES = ()


def is_historic_record(rel):
    """Report whether a spec-relative path is a dated record we keep verbatim."""
    return (len(rel.parts) > 2 and len(rel.parts[2]) == 4 and rel.parts[2].isdigit()
            and any(rel.parts[:2] == prefix for prefix in SKIP_PREFIXES))


def walk(root, include_records):
    """Yields the Markdown files under a directory that a sweep may rewrite."""
    for path in root.rglob("*.md"):
        rel = path.relative_to(REPO_ROOT)
        # "generated" is refused here as well as in select_files, so a repository that leaves it
        # out of SKIP_DIRS still cannot have a sweep rewrite what "make generate" reproduces.
        if (SKIP_DIRS & set(rel.parts) or "generated" in rel.parts
                or (not include_records and is_historic_record(rel))):
            continue
        yield path


def select_files(paths, include_records=False, excluded=()):
    """Returns the files to format, plus a message per argument that names nothing formattable.

    A file named as an argument is formatted even where a sweep skips its directory, so a single
    record or skill file can be aligned in place. Only `generated/` stays off limits, because it
    is reproduced by `make generate` rather than edited.
    """
    skipped = {(REPO_ROOT / e).resolve() for e in excluded}
    found, rejected = set(), []

    for arg in paths or [REPO_ROOT]:
        path = (REPO_ROOT / arg).resolve()

        if path != REPO_ROOT and REPO_ROOT not in path.parents:
            rejected.append(f"{arg}: outside the repository")
        elif path.is_dir():
            found |= set(walk(path, include_records))
        elif not path.is_file():
            rejected.append(f"{arg}: no such file or directory")
        elif "generated" in path.relative_to(REPO_ROOT).parts:
            rejected.append(f"{arg}: generated, run \"make generate\" instead")
        else:
            found.add(path)

    return sorted(found - skipped), rejected


def main():
    # Options are matched explicitly and anything unrecognized is refused, because the default
    # action rewrites every Markdown file in the tree: an option this script merely ignored
    # (a typo, or --help) would run that sweep by surprise instead of reporting the mistake.
    args = sys.argv[1:]

    check = False
    include_records = False
    show_help = False
    excluded = set()
    paths = []
    i = 0

    while i < len(args):
        if args[i] in ("--help", "-h"):
            # Recorded rather than acted on, so the loop still validates the rest: help must not
            # become a way to slip an unrecognized option past the guard below.
            show_help = True
        elif args[i] == "--check":
            check = True
        elif args[i] == "--all":
            include_records = True
        elif args[i] == "--exclude":
            # The value is checked, not just counted: consuming an option-shaped token here would
            # carry it past the guard below, so "--exclude --check" would drop the check and
            # rewrite the tree while reporting success.
            if i + 1 >= len(args) or args[i + 1].startswith("-"):
                print("format-tables: --exclude requires a path", file=sys.stderr)
                return 2
            excluded.add(REPO_ROOT / args[i + 1])
            i += 1
        elif args[i].startswith("-"):
            print(f"format-tables: unknown option {args[i]!r} (try --help)", file=sys.stderr)
            return 2
        else:
            paths.append(args[i])
        i += 1

    if show_help:
        print((__doc__ or "").strip())
        return 0

    if not shutil.which("npx"):
        print("format-tables: npx not found; install Node.js to use this target.", file=sys.stderr)
        return 1

    files, rejected = select_files(paths, include_records, excluded)

    for note in rejected:
        print(f"[ERROR] {note}", file=sys.stderr)

    if not files:
        print("Tables: nothing to format.", file=sys.stderr)
        return 1 if rejected else 0

    changed = [str(p.relative_to(REPO_ROOT)) for p in format_batch(files, check)]

    if check and changed:
        for name in changed:
            print(f"[ERROR] Table drift: {name}", file=sys.stderr)
        print(f"Table check failed for {len(changed)} of {len(files)} files.", file=sys.stderr)
        return 1

    verb = "would reformat" if check else "reformatted"
    print(f"Tables {'check passed' if check else 'formatted'} "
          f"({len(files)} files checked, {len(changed)} {verb}).")

    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main())
