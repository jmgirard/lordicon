#!/usr/bin/env python3
"""Check the attributes of each <lord-icon> made from _tests/aria.qmd against
the expected values below, in two places:

- page: the HTML page Quarto renders from the fixture.
- filter: the raw HTML each shortcode returns, from raw_output.lua. Quarto's
  HTML post-processing keeps only one of two same-name attributes, so only
  this output shows an attribute the filter wrote twice. The parser
  lowercases attribute names, so the check also reads this output as text to
  confirm that each forwarded key keeps the spelling the user wrote.

It also checks the attribute order of the cases in ORDER, the lordicon
warnings in the render's log against WARNED, and that a render of the fixture
to gfm gives no <lord-icon> and no lordicon warning.

The fixture renders in a temporary directory, so the demo site in docs/ is
not touched. Exits 1 when any check fails. Usage: python3 _tests/check_aria.py
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
    "bad-empty": "",
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

# Cases whose <lord-icon> holds no attribute beyond `id`, `src`, and the ones
# CASES gives a value. The `label` case shows that `label` is not passed on.
EXACT = {"src-li", "src-lif", "src-upper", "kept-names", "label", *BAD}

# Keys that differ only in letter case give one attribute name more than once
# in the filter output, which the parser lowercases. The page keeps one.
CLASH = {
    "clash-role": {"aria-hidden": None, "aria-label": None},
    "clash-class": DECORATIVE,
    "clash-arialabel": {"aria-hidden": None, "role": None},
    "clash-two": {"aria-hidden": None, "aria-label": None},
    "clash-accent": DECORATIVE,
}
CASES.update(CLASH)
CASES["clash-empty"] = {"aria-hidden": None, "role": "img", "aria-label": None}

# How many times each case's clashing names appear in the filter output.
TWICE = {
    "clash-role": {"role": 2},
    "clash-class": {"class": 3},
    "clash-arialabel": {"aria-label": 2},
    "clash-two": {"role": 2, "data-x": 2},
    "clash-accent": {"data-é": 2},
    "label-two": {"label": 2},
}

# Only a lowercase `label` labels the icon. A key such as `Label` passes on.
CASES["label-upper"] = {**DECORATIVE, "label": "Bell"}
CASES["label-mixed"] = {"aria-hidden": None, "role": "img", "aria-label": "Bell", "label": "Ring"}
CASES["label-two"] = DECORATIVE

# minified.json has no control layer, as in a Minified export; gift_raw.json
# has one.
CASES["minified-lif"] = DECORATIVE
CASES["raw-lif"] = DECORATIVE
# The Minified warning fires once per path as written: a second call on
# minified.json gives none, and ./minified.json gives its own.
CASES["minified-again"] = DECORATIVE
CASES["minified-dotslash"] = DECORATIVE

# An argument that Quarto cannot read bare is quoted in the warning's call.
CASES["quoted-space"] = {"src": "mini fied.json", **DECORATIVE}
CASES["quoted-dquote"] = {"src": 'https://cdn.lordicon.com/a "b" c\\d.json', **DECORATIVE}
CASES["quoted-equals"] = {"src": "https://cdn.lordicon.com/x=y.json", **DECORATIVE}
CASES["quoted-backslash"] = {"src": "https://cdn.lordicon.com/a\\b.json", **DECORATIVE}

SHOWN ={"aria-hidden": None, "aria-label": None}
CASES.update({
    "nameless-img": {**SHOWN, "role": "img"},
    "nameless-upper": {**SHOWN, "role": "IMG"},
    "nameless-image": {**SHOWN, "role": "image"},
    "nameless-first": {**SHOWN, "role": "img presentation"},
    "nameless-shown": {"aria-hidden": "false", "role": "img", "aria-label": None},
    "nameless-hidden-clash": {"role": "img", "aria-label": None},
    "named-arialabel": {"aria-hidden": None, "role": "img", "aria-label": "Bell"},
    "named-labelledby": {**SHOWN, "role": "img", "aria-labelledby": "caption"},
    "named-title": {**SHOWN, "role": "img", "title": "Bell"},
    "named-title-upper": {**SHOWN, "role": "img", "title": "Bell"},
    "named-label": {"aria-hidden": None, "role": "img", "aria-label": "Bell"},
    "named-hidden-attr": {**SHOWN, "role": "img", "hidden": "hidden"},
    "named-inert": {**SHOWN, "role": "img", "inert": "inert"},
    "named-aria-hidden": {"aria-hidden": "true", "role": "img", "aria-label": None},
    "named-aria-hidden-upper": {"aria-hidden": "TRUE", "role": "img", "aria-label": None},
    "named-first-presentation": {**SHOWN, "role": "presentation img"},
    "named-role-clash": SHOWN,
})
# The role is the first token that names a role in the filter's ARIA list.
AFTER_TOKENS = {
    "nameless-after-bogus": "bogus img",
    "nameless-after-abstract": "landmark img",
    "nameless-after-upper": "BOGUS Img",
    "nameless-two-spaces": "bogus  img",
    "nameless-after-bogus-image": "bogus image",
    "nameless-symbol": "graphics-symbol",
    "nameless-symbol-img": "graphics-symbol img",
    "nameless-after-bogus-symbol": "bogus graphics-symbol",
    "nameless-symbol-mixed": "Graphics-Symbol img",
}
OTHER_FIRST = {
    "named-bogus-presentation": "bogus presentation img",
    "named-button": "button img",
    "named-doc-cover": "doc-cover img",
    "named-graphics-document": "graphics-document img",
    "named-bogus": "bogus",
    "named-nbsp": "bogus img",
}
for case, role in {**AFTER_TOKENS, **OTHER_FIRST}.items():
    CASES[case] = {**SHOWN, "role": role}
CASES["named-symbol-label"] = {"aria-hidden": None, "role": "bogus graphics-symbol", "aria-label": "Bell"}
CASES["named-symbol-hidden"] = {"aria-hidden": "true", "role": "graphics-symbol", "aria-label": None}
TWICE["nameless-hidden-clash"] = {"aria-hidden": 2}
TWICE["named-role-clash"] = {"role": 2}

# The attribute names of each case, in order: `src`, the forwarded keys in
# byte order, then the ARIA defaults. The parser lowercases `Zeta`, which
# sorts before `class` only by byte.
CASES["sorted"] = DECORATIVE
ORDER = {
    "sorted": ["src", "@click", "zeta", "class", "data-a", "id", "trigger", "aria-hidden"],
}

# The value the page keeps of names that appear twice: the first in the
# filter's byte order. `dict(attrs)` in check() keeps the last, so only the
# page is checked.
PAGE_ONLY = {
    "clash-role": {"role": "img"},
    "clash-two": {"role": "img"},
    "nameless-hidden-clash": {"aria-hidden": "false"},
    "named-role-clash": {"role": "presentation"},
}

# The lordicon warnings of each case. Each warning is a list of texts that one
# line of the render's log must hold, where CALL stands for the case's call,
# such as {{< li CODE >}}. No other lordicon warning may appear in the log.
CALL = object()
SKIPS = {"src-li": "src", "src-lif": "src", "src-upper": "SRC", **BAD}
WARNED = {case: [[CALL, "skips the", f'"{key}"']] for case, key in SKIPS.items()}
CASE_CLASH = "differ only in letter case"
ONE = "The page keeps only one of their values."
EACH = "The page keeps only one value from each group."
WARNED.update({
    "clash-role": [[CALL, CASE_CLASH, '"Role" and "role".', ONE]],
    "clash-class": [[CALL, CASE_CLASH, '"CLASS", "Class", and "class".', ONE]],
    "clash-arialabel": [[CALL, CASE_CLASH, '"aria-Label" and "aria-label".', ONE]],
    "clash-two": [[CALL, CASE_CLASH, '"DATA-X" and "data-x"; "ROLE" and "role".', EACH]],
    "clash-accent": [[CALL, CASE_CLASH, '"data-É" and "data-é".', ONE]],
})
LABEL_CASE = "only a lowercase label key labels the icon. Use one lowercase label key."
WARNED.update({
    "label-upper": [[CALL, LABEL_CASE, 'the key "Label",']],
    "label-mixed": [[CALL, LABEL_CASE, 'the key "laBel",']],
    "label-two": [[CALL, LABEL_CASE, 'the keys "LABEL" and "Label",']],
    "minified-lif": [
        [CALL, "looks like a Minified Lottie export", "so Colors, STROKE, sTaTe will"]
    ],
    "minified-dotslash": [[CALL, "looks like a Minified Lottie export", "so colors will"]],
})
NAMELESS = "but no name, so a screen reader announces an image"
FIX = 'Add a label, such as label="Bell".'
for case, role in {
    "nameless-img": "img",
    "nameless-upper": "IMG",
    "nameless-image": "image",
    "nameless-first": "img presentation",
    "nameless-shown": "img",
    "nameless-hidden-clash": "img",
    "clash-role": "img",
    "clash-two": "img",
    "clash-empty": "img",
    **AFTER_TOKENS,
}.items():
    WARNED.setdefault(case, []).append([CALL, f'role="{role}"', NAMELESS, FIX])
WARNED["nameless-hidden-clash"].append(
    [CALL, CASE_CLASH, '"ARIA-HIDDEN" and "aria-hidden".', ONE]
)
WARNED["named-role-clash"] = [[CALL, CASE_CLASH, '"Role" and "role".', ONE]]
# These calls are written out, not built from the argument, because the
# warning quotes the argument as Quarto reads it back.
WARNED.update({
    "quoted-space": [
        ['{{< lif "mini fied.json" >}}', "looks like a Minified Lottie export", "so colors will"]
    ],
    "quoted-dquote": [["{{< li 'a \"b\" c\\\\d' >}}", "skips the", '"src"']],
    "quoted-equals": [['{{< li "x=y" >}}', "skips the", '"src"']],
    "quoted-backslash": [['{{< li "a\\\\b" >}}', "skips the", '"src"']],
})

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


def render(to, output):
    """Render the fixture to a format, returning the output file's text and
    the render's log."""
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        shutil.copytree(ROOT / "_extensions", workdir / "_extensions")
        shutil.copy(FIXTURE, workdir)
        shutil.copy(ROOT / "gift_raw.json", workdir)
        shutil.copy(ROOT / "_tests" / "minified.json", workdir)
        shutil.copy(ROOT / "_tests" / "minified.json", workdir / "mini fied.json")
        cmd = ["quarto", "render", "aria.qmd", "--to", to]
        done = run(cmd, workdir, {**os.environ, "LC_ALL": "C.UTF-8"})
        return (workdir / output).read_text(encoding="utf-8"), done.stderr


def check_non_html():
    """A render to a format other than HTML gives no icon and no warning."""
    text, log = render("gfm", "aria.md")
    failures = [f"gfm: the output holds {s!r}" for s in ("lord-icon", "{{<") if s in text]
    lines = [line for line in log.split("\n") if "lordicon:" in line]
    failures += [f"gfm: warning {line!r}" for line in lines]
    print(f"gfm: {len(text)} characters and {len(lines)} lordicon warnings read")
    return failures


def unquote(part):
    # Inside quotes, Quarto reads `\\` as `\`.
    return part[1:-1].replace("\\\\", "\\") if part[0] in "\"'" else part


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
        # check covers both. A C library that classifies no byte from 128 up
        # in a UTF-8 locale (glibc) makes the two runs alike.
        return run(cmd, ROOT, {**os.environ, "LC_ALL": "C"}).stdout


def check_spelling(calls, raw):
    """Each forwarded key appears in the raw output as the user wrote it."""
    failures = []
    # Split on "\n" alone: splitlines() also breaks at U+0085, a C1 control.
    for call, line in zip(calls, raw.rstrip("\n").split("\n"), strict=True):
        for key, value in call["kwargs"].items():
            skipped = (
                key in ("label", "") or key.lower() == "src" or INVALID_NAME.search(key)
            )
            if value and not skipped and f' {key}="' not in line:
                failures.append(f"filter {call['kwargs'].get('id')}: no {key}= in {line}")
    return failures


def check_warnings(calls, log):
    """Each warning in WARNED matches exactly one lordicon line of the log."""
    lines = [line for line in log.split("\n") if "lordicon:" in line]
    failures = []
    expected = 0
    for call in calls:
        case = call["kwargs"].get("id")
        name = f"{{{{< {call['shortcode']} {call['arg']} >}}}}"
        for warning in WARNED.get(case, []):
            texts = [name if text is CALL else text for text in warning]
            found = [line for line in lines if all(text in line for text in texts)]
            if len(found) != 1:
                failures.append(f"log {case}: {len(found)} warnings hold {texts!r}")
            expected += 1
    if len(lines) != expected:
        failures.append(f"log: {len(lines)} lordicon warnings, expected {expected}")
    print(f"log: {len(lines)} lordicon warnings read, {expected} expected")
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
        allowed = TWICE.get(case, {}) if where == "filter" else {}
        dupes = sorted({
            n for n in names if names.count(n) > 1 and names.count(n) != allowed.get(n)
        })
        if dupes:
            failures.append(f"{where} {case}: attribute twice: {', '.join(dupes)}")
        if case not in CASES:
            failures.append(f"{where} {case}: <lord-icon> with no expected case")
            continue
        seen.add(case)
        if case in ORDER and names != ORDER[case]:
            failures.append(f"{where} {case}: attribute order is {names}, expected {ORDER[case]}")
        expected = CASES[case]
        if where == "page":
            expected = {**expected, **PAGE_ONLY.get(case, {})}
        for name, want in expected.items():
            got = values.get(name)
            if got != want:
                failures.append(f"{where} {case}: {name} is {got!r}, expected {want!r}")
        if case in EXACT:
            allowed = {"id", "src"} | {n for n, want in CASES[case].items() if want is not None}
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
    page, log = render("html", "aria.html")
    raw = filter_output(calls)
    failures = (
        check("page", page)
        + check("filter", raw)
        + check_spelling(calls, raw)
        + check_warnings(calls, log)
        + check_non_html()
    )
    for line in failures:
        print("FAIL", line)
    print(f"{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
