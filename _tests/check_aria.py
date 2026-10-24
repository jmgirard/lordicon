#!/usr/bin/env python3
"""Check the attributes of each <lord-icon> made from _tests/aria.qmd against
the expected values below, in two places:

- page: the HTML page Quarto renders from the fixture.
- filter: the raw HTML each shortcode returns, from raw_output.lua. Quarto's
  HTML post-processing keeps only the first of two same-name attributes, so
  only this output shows an attribute the filter wrote twice. The parser
  lowercases attribute names, so the check also reads this output as text to
  confirm that each forwarded key keeps the spelling the user wrote.

It also checks the lordicon warnings in the render's log against WARNED.

The fixture renders in a temporary directory, so the demo site in docs/ is
not touched. Exits 1 when a case fails. Usage: python3 _tests/check_aria.py
"""

import json
import os
import re
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

# An ARIA name in another letter case acts as the lowercase name does.
for case, twin in {
    "hidden-mixed": "hidden-li",
    "arialabel-upper": "arialabel-li",
    "labelledby-mixed": "labelledby-li",
    "role-upper": "role-li",
    "label-role-mixed": "label-role",
    "label-arialabel-mixed": "label-arialabel",
}.items():
    CASES[case] = CASES[twin]

# A src key never replaces the first argument's source.
ICON = "https://cdn.lordicon.com/wlpxtupd.json"
DECORATIVE = {"aria-hidden": "true", "role": None, "aria-label": None}
CASES["src-li"] = {"src": ICON, **DECORATIVE}
CASES["src-lif"] = {"src": "gift_raw.json", **DECORATIVE}
CASES["src-upper"] = {"src": ICON, **DECORATIVE}

# A key that is not a valid attribute name gives no attribute.
BAD = {
    "bad-space": "a b",
    "bad-dquote": 'a"b',
    "bad-squote": "a'b",
    "bad-gt": "a>b",
    "bad-slash": "a/b",
    "bad-equals": "a=b",
    "bad-c1": "a\x85b",
    "bad-control": "a\x01b",
}
for case in BAD:
    CASES[case] = {"src": ICON, "class": "big", **DECORATIVE}

# Keys that are valid attribute names, though they hold symbols or letters
# outside ASCII, pass through unchanged.
CASES["kept-names"] = {
    "src": ICON,
    "@click": "2",
    "data.k": "3",
    "data-straße": "4",
    "data-datà": "5",
    **DECORATIVE,
}

# Cases whose <lord-icon> holds no attribute beyond `id` and the ones CASES
# gives a value.
EXACT = {"src-li", "src-lif", "src-upper", "kept-names", *BAD}

# The key that the one lordicon warning of each case must name. No other
# lordicon warning may appear in the render's log.
WARNED = {"src-li": "src", "src-lif": "src", "src-upper": "SRC", **BAD}

# The characters that the filter skips a key for: its INVALID_NAME pattern
# (space, the ASCII controls, `"'>/=`) and its C1_CONTROL pattern
# (U+0080 to U+009F).
INVALID_NAME = re.compile(r"[\x00-\x20\x7f-\x9f\"'>/=]")

# One shortcode argument: a key=value pair or a positional word. A key or a
# value may be quoted, and a quoted key may hold `=`.
QUOTED = r""""[^"]*"|'[^']*'"""
ITEM = re.compile(
    rf"""\s*(?:(?P<key>{QUOTED}|[^\s"'=]+)=(?P<value>{QUOTED}|[^\s"']+)"""
    rf"""|(?P<word>{QUOTED}|[^\s"']+))"""
)


class IconParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.icons = []  # one list of (name, value) pairs per <lord-icon>

    def handle_starttag(self, tag, attrs):
        if tag == "lord-icon":
            self.icons.append(attrs)


def run(cmd, cwd, env=None):
    """Run a command, printing its output and exiting 1 when it fails."""
    done = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if done.returncode != 0:
        print(f"FAIL `{' '.join(cmd)}` exited {done.returncode}")
        print(done.stdout + done.stderr)
        sys.exit(1)
    return done


def render_page():
    """Render the fixture, returning the page and the render's log."""
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        shutil.copytree(ROOT / "_extensions", workdir / "_extensions")
        shutil.copy(FIXTURE, workdir)
        shutil.copy(ROOT / "gift_raw.json", workdir)
        cmd = ["quarto", "render", "aria.qmd", "--to", "html"]
        done = run(cmd, workdir, {**os.environ, "LC_ALL": "C.UTF-8"})
        return (workdir / "aria.html").read_text(encoding="utf-8"), done.stderr


def unquote(part):
    return part[1:-1] if part[0] in "\"'" else part


def fixture_calls():
    """Read each li or lif shortcode call from the fixture."""
    calls = []
    for body in re.findall(r"\{\{<\s*(lif?\s.*?)\s*>\}\}", FIXTURE.read_text()):
        words, kwargs, pos = [], {}, 0
        while pos < len(body):
            item = ITEM.match(body, pos)
            if not item:
                sys.exit(f"FAIL cannot read the fixture call {{{{< {body} >}}}}")
            if item["key"]:
                kwargs[unquote(item["key"])] = unquote(item["value"])
            else:
                words.append(unquote(item["word"]))
            pos = item.end()
        shortcode, arg = words
        calls.append({"shortcode": shortcode, "arg": arg, "kwargs": kwargs})
    return calls


def filter_output(calls):
    with tempfile.TemporaryDirectory() as tmp:
        cases = Path(tmp) / "cases.json"
        cases.write_text(json.dumps(calls))
        cmd = ["quarto", "pandoc", "lua", "_tests/raw_output.lua", str(cases)]
        # Lua's character classes follow the process locale. The page renders
        # under a UTF-8 locale and this output under the C locale, so the
        # check covers both.
        return run(cmd, ROOT, {**os.environ, "LC_ALL": "C"}).stdout


def check_spelling(calls, raw):
    """Each forwarded key appears in the raw output as the user wrote it."""
    failures = []
    # Split on "\n" alone: splitlines() also breaks at U+0085, a C1 control.
    for call, line in zip(calls, raw.rstrip("\n").split("\n"), strict=True):
        for key, value in call["kwargs"].items():
            skipped = key == "label" or key.lower() == "src" or INVALID_NAME.search(key)
            if value and not skipped and f' {key}="' not in line:
                failures.append(f"filter {call['kwargs'].get('id')}: no {key}= in {line}")
    return failures


def check_warnings(calls, log):
    """Each WARNED case gives one lordicon warning naming its call and key."""
    lines = [line for line in log.split("\n") if "lordicon:" in line]
    failures = []
    for call in calls:
        case = call["kwargs"].get("id")
        if case not in WARNED:
            continue
        name = f"{{{{< {call['shortcode']} {call['arg']} >}}}}"
        found = [line for line in lines if name in line and f'"{WARNED[case]}"' in line]
        if len(found) != 1:
            failures.append(f"log {case}: {len(found)} warnings name {name} and {WARNED[case]!r}")
    if len(lines) != len(WARNED):
        failures.append(f"log: {len(lines)} lordicon warnings, expected {len(WARNED)}")
    print(f"log: {len(lines)} lordicon warnings read, {len(WARNED)} expected")
    return failures


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
        if case in EXACT:
            allowed = {"id"} | {name for name, want in CASES[case].items() if want is not None}
            extra = sorted(set(names) - allowed)
            if extra:
                failures.append(f"{where} {case}: unexpected attributes: {', '.join(extra)}")

    for case in CASES:
        if case not in seen:
            failures.append(f"{where} {case}: no <lord-icon> in the output")
    print(f"{where}: {len(parser.icons)} icons read, {len(CASES)} cases")
    return failures


def main():
    calls = fixture_calls()
    page, log = render_page()
    raw = filter_output(calls)
    failures = (
        check("page", page)
        + check("filter", raw)
        + check_spelling(calls, raw)
        + check_warnings(calls, log)
    )
    for line in failures:
        print("FAIL", line)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
