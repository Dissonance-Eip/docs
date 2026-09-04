#!/usr/bin/env python3
"""Check every Markdown file in this repository against DOCUMENTATION_STANDARD.md.

Enforces only the mechanical rules — front matter and its required fields, a
single ATX H1, filename shape, ISO dates, bullet markers, tagged code fences,
leftover template headers. Judgement calls (is the summary a conclusion? is the
status honest?) stay with the reviewer.

Usage:
    python3 scripts/check-docs.py [path ...]     # defaults to the repo root

Exits 0 when clean, 1 when any file has a violation.
"""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED_FIELDS = ("title", "status", "owner", "created", "updated")
VALID_STATUS = {"draft", "review", "final", "active", "superseded"}

# Root-level documents that conventionally keep an uppercase filename.
UPPERCASE_ALLOWED = {"README.md", "CONTRIBUTING.md", "DOCUMENTATION_STANDARD.md"}
# GitHub renders these two without front matter; adding one would show up as text.
NO_FRONT_MATTER = {"README.md", "CONTRIBUTING.md"}
# GitHub owns the names and front-matter schema of everything under .github/.
# A benchmark's results/ holds generated data, not documents.
EXEMPT_DIRS = {".github", ".git", "node_modules", "results"}

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")
GOOD_NAME = re.compile(r"^[a-z0-9]+(?:[-.][a-z0-9]+)*\.md$")


def parse_front_matter(lines: list[str]) -> dict[str, str] | None:
    """Return the front-matter fields, or None when the block is absent."""
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None
    fields = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "-", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def strip_fences(body: list[str]) -> list[str]:
    """Blank out fenced code blocks so their contents are not read as Markdown."""
    out, in_fence = [], False
    for line in body:
        if line.startswith("```"):
            in_fence = not in_fence
            out.append("")
        else:
            out.append("" if in_fence else line)
    return out


def check(path: pathlib.Path, root: pathlib.Path) -> list[str]:
    rel = path.relative_to(root)
    # Templates carry placeholder front matter and instructional comments by
    # design; only their shape is checked.
    is_template = "templates" in rel.parts
    problems: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    # --- filename ---------------------------------------------------------
    if path.name not in UPPERCASE_ALLOWED and not GOOD_NAME.match(path.name):
        if DATE_PREFIX.match(path.name):
            stem = path.name[11:]
            if not GOOD_NAME.match(stem):
                problems.append("filename: use lowercase kebab-case after the date prefix")
        else:
            problems.append("filename: use lowercase kebab-case, ASCII only")

    # --- front matter -----------------------------------------------------
    fields = parse_front_matter(lines)
    if path.name in NO_FRONT_MATTER:
        body_start = 0
    elif fields is None:
        problems.append("front matter: missing")
        body_start = 0
    else:
        for field in REQUIRED_FIELDS:
            if field not in fields:
                problems.append(f"front matter: missing required field '{field}'")
        status = fields.get("status")
        if status and status not in VALID_STATUS:
            problems.append(
                f"front matter: status '{status}' is not one of {sorted(VALID_STATUS)}")
        if not is_template:
            for field in ("created", "updated"):
                value = fields.get(field)
                if value and not ISO_DATE.match(value):
                    problems.append(f"front matter: {field} '{value}' is not an ISO date")
        body_start = next(i for i in range(1, len(lines)) if lines[i].strip() == "---") + 1

    # --- headings ---------------------------------------------------------
    body = strip_fences(lines[body_start:])
    h1s = [i for i, line in enumerate(body) if line.startswith("# ")]
    if not h1s:
        problems.append("headings: no ATX '# ' heading")
    elif len(h1s) > 1:
        problems.append(f"headings: {len(h1s)} '# ' headings, expected exactly 1")
    else:
        first_heading = next(
            (line for line in body if line.startswith("#")), "")
        if not first_heading.startswith("# "):
            problems.append("headings: document opens below H1")
        if fields:
            title = fields.get("title", "")
            heading = body[h1s[0]][2:].strip()
            if title and heading != title:
                problems.append("headings: H1 does not match front-matter title")

    for i, line in enumerate(body):
        if re.match(r"^=+\s*$", line) and i and body[i - 1].strip():
            problems.append("headings: setext heading — use '# ' instead")
            break

    # --- body formatting --------------------------------------------------
    in_fence = False
    for line in body:
        fence = re.match(r"^```(\w*)", line)
        if fence:
            if not in_fence and not fence.group(1):
                problems.append("code fence: opened without a language tag")
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^\* ", line):
            problems.append("bullets: '*' used — use '-'")
            break

    for line in body:
        if re.match(r"^ +- ", line) and not re.match(r"^ {2,}- ", line):
            problems.append("bullets: single-space indent — start '-' at column zero")
            break

    if not is_template and re.search(
            r"^(Meeting notes template|Issue template)\s*$", text, re.M):
        problems.append("content: template header left in a real document")

    return [f"{rel}: {p}" for p in problems]


def main(argv: list[str]) -> int:
    root = pathlib.Path(__file__).resolve().parent.parent
    targets = [pathlib.Path(a) for a in argv[1:]] or [root]

    files: list[pathlib.Path] = []
    for target in targets:
        if target.is_file():
            files.append(target.resolve())
        else:
            files += [
                p for p in sorted(target.resolve().rglob("*.md"))
                if not EXEMPT_DIRS & set(p.relative_to(root).parts)
            ]

    problems = [p for f in files for p in check(f, root)]
    for problem in problems:
        print(problem)

    print(f"\n{len(files) - len({p.split(':')[0] for p in problems})}"
          f"/{len(files)} files clean, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
