#!/usr/bin/env python3
"""Check the ARIA attributes of each <lord-icon> made from _tests/aria.qmd
against the expected values below, in two places:

- page: the HTML page Quarto renders from the fixture.
- filter: the raw HTML each shortcode returns, from raw_output.lua. Quarto's
  HTML post-processing keeps only the first of two same-name attributes, so
  only this output shows an attribute the filter wrote twice.

The fixture renders in a temporary directory, so the demo site in docs/ is
not touched. Exits 1 when a case fails. Usage: python3 _tests/check_aria.py
"""

import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "_tests" / "aria.qmd"

TRICKY = 'Tom & "Jerry"'

# Expected value of each ARIA attribute per case id; None means absent.
CASES = {
    "hidden-li": {"aria-hidden": "false", "role": None, "aria-label": None},
    "arialabel-li": {"aria-hidden": None, "role": None, "aria-label": "Bell"},
    "labelledby-li": {
        "aria-hidden": None,
        "role": None,
        "aria-label": None,
        "aria-labelledby": "caption",
    },
    "role-li": {"aria-hidden": None, "role": "presentation", "aria-label": None},
    "arialabel-lif": {"aria-hidden": None, "role": None, "aria-label": "Gift"},
    "arialabel-escaped": {"aria-hidden": None, "role": None, "aria-label": TRICKY},
    "bare": {"aria-hidden": "true", "role": None, "aria-label": None},
    "empty-arialabel": {"aria-hidden": "true", "role": None, "aria-label": None},
    "empty-label": {"aria-hidden": "true", "role": None, "aria-label": None},
    "describedby": {
        "aria-hidden": "true",
        "role": None,
        "aria-label": None,
        "aria-describedby": "caption",
    },
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


def run(cmd, cwd):
    """Run a command, printing its output and exiting 1 when it fails."""
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        print(f"FAIL `{' '.join(cmd)}` exited {done.returncode}")
        print(done.stdout + done.stderr)
        sys.exit(1)
    return done.stdout


def render_page():
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        shutil.copytree(ROOT / "_extensions", workdir / "_extensions")
        shutil.copy(FIXTURE, workdir)
        shutil.copy(ROOT / "gift_raw.json", workdir)
        run(["quarto", "render", "aria.qmd", "--to", "html"], workdir)
        return (workdir / "aria.html").read_text(encoding="utf-8")


def fixture_calls():
    """Read each li or lif shortcode call from the fixture."""
    calls = []
    for body in re.findall(r"\{\{<\s*(lif?\s.*?)\s*>\}\}", FIXTURE.read_text()):
        shortcode, arg, *pairs = shlex.split(body)
        kwargs = dict(pair.split("=", 1) for pair in pairs)
        calls.append({"shortcode": shortcode, "arg": arg, "kwargs": kwargs})
    return calls


def filter_output():
    with tempfile.TemporaryDirectory() as tmp:
        cases = Path(tmp) / "cases.json"
        cases.write_text(json.dumps(fixture_calls()))
        return run(["quarto", "pandoc", "lua", "_tests/raw_output.lua", str(cases)], ROOT)


def check(where, html):
    parser = IconParser()
    parser.feed(html)
    failures = []
    seen = set()

    for attrs in parser.icons:
        names = [name for name, _ in attrs]
        values = dict(attrs)
        case = values.get("id")
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            failures.append(f"{where} {case}: attribute twice: {', '.join(dupes)}")
        if case not in CASES:
            failures.append(f"{where} {case}: <lord-icon> with no expected case")
            continue
        seen.add(case)
        for name, want in CASES[case].items():
            got = values.get(name)
            if got != want:
                failures.append(f"{where} {case}: {name} is {got!r}, expected {want!r}")

    for case in CASES:
        if case not in seen:
            failures.append(f"{where} {case}: no <lord-icon> in the output")
    print(f"{where}: {len(parser.icons)} icons read, {len(CASES)} cases")
    return failures


def main():
    failures = check("page", render_page()) + check("filter", filter_output())
    for line in failures:
        print("FAIL", line)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
