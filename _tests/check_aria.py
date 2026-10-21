#!/usr/bin/env python3
"""Render _tests/aria.qmd with the extension and check the ARIA attributes
of each <lord-icon> element against the expected values below.

The fixture renders in a temporary directory, so the demo site in docs/ is
not touched. Exits 1 when a case fails. Usage: python3 _tests/check_aria.py
"""

import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TRICKY = 'Tom & "Jerry"'

# Expected value of each ARIA attribute per case id; None means absent.
CASES = {
    "hidden-li": {"aria-hidden": "false", "role": None, "aria-label": None},
    "arialabel-li": {"aria-hidden": None, "role": None, "aria-label": "Bell"},
    "labelledby-li": {"aria-hidden": None, "aria-labelledby": "caption"},
    "role-li": {"aria-hidden": None, "role": "presentation", "aria-label": None},
    "arialabel-lif": {"aria-hidden": None, "role": None, "aria-label": "Gift"},
    "arialabel-escaped": {"aria-hidden": None, "aria-label": TRICKY},
    "bare": {"aria-hidden": "true", "role": None, "aria-label": None},
    "empty-arialabel": {"aria-hidden": "true", "role": None, "aria-label": None},
    "empty-label": {"aria-hidden": "true", "role": None, "aria-label": None},
    "describedby": {"aria-hidden": "true", "aria-describedby": "caption"},
    "label": {"aria-hidden": None, "role": "img", "aria-label": "Bell"},
    "label-role": {"aria-hidden": None, "role": "presentation", "aria-label": "Bell"},
    "label-arialabel": {"aria-hidden": None, "role": "img", "aria-label": "Other"},
    "label-both": {"aria-hidden": None, "role": "presentation", "aria-label": "Other"},
    "label-escaped": {"aria-hidden": None, "role": "img", "aria-label": TRICKY},
}


class IconParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.icons = []  # one list of (name, value) pairs per <lord-icon>

    def handle_starttag(self, tag, attrs):
        if tag == "lord-icon":
            self.icons.append(attrs)


def render(workdir):
    shutil.copytree(ROOT / "_extensions", workdir / "_extensions")
    shutil.copy(ROOT / "_tests" / "aria.qmd", workdir)
    shutil.copy(ROOT / "gift_raw.json", workdir)
    subprocess.run(
        ["quarto", "render", "aria.qmd", "--to", "html"],
        cwd=workdir,
        check=True,
        capture_output=True,
    )
    return (workdir / "aria.html").read_text(encoding="utf-8")


def check(html):
    parser = IconParser()
    parser.feed(html)
    failures = []
    seen = {}

    for attrs in parser.icons:
        names = [name for name, _ in attrs]
        values = dict(attrs)
        case = values.get("id")
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            failures.append(f"{case}: attribute twice: {', '.join(dupes)}")
        if case not in CASES:
            failures.append(f"{case}: <lord-icon> with no expected case")
            continue
        seen[case] = True
        for name, want in CASES[case].items():
            got = values.get(name)
            if got != want:
                failures.append(f"{case}: {name} is {got!r}, expected {want!r}")

    for case in CASES:
        if case not in seen:
            failures.append(f"{case}: no <lord-icon> in the rendered fixture")
    return len(parser.icons), failures


def main():
    with tempfile.TemporaryDirectory() as tmp:
        html = render(Path(tmp))
    count, failures = check(html)
    for line in failures:
        print("FAIL", line)
    print(f"{count} icons read, {len(CASES)} cases, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
