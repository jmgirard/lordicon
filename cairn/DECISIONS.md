# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001 (2026-10-20): The extension version rises at each shipping merge

**Context:** `quarto add jmgirard/lordicon` installs from `main`, so every merge reaches users at once; history already raised `_extension.yml` with each change (09a2e5f, 825985a).
**Decision:** Each merge that ships a user-visible change raises `version:` in `_extension.yml`; the `v<version>` tag follows the merge.
**Consequences:** `/cairn-release` takes its tag-only arm for these versions; considered raising only at release time, rejected because users on `main` would get changes under an old number.

### D-002 (2026-10-20): Keep a CHANGELOG.md

**Context:** Users of `quarto add` see no commit log, and release notes so far came only from commit subjects.
**Decision:** The repo keeps `CHANGELOG.md`, with an entry for each user-visible change; the PROFILE `changelog` slot names it.
**Consequences:** The review consistency gate checks for an entry in each milestone; the file is created by a candidate milestone, and until it exists the slot reads as none.

### D-003 (2026-10-20): Reserve `src` and skip invalid attribute names (narrows IP1 and IP5)

**Context:** A user `src` key gives a second `src` attribute, and Quarto's HTML post-processing drops it. A key that holds whitespace, a control character, `"`, `'`, `>`, `/`, or `=` gives broken markup or stray attributes. IP1 says every user attribute reaches `<lord-icon>` unchanged. IP5 asks for one warning release before the passthrough meaning breaks.
**Decision:** The user chose both changes at the M003 plan gate. A `src` key in any letter case is reserved like `label`: the first argument's source stays, and the render warns. A key that HTML does not allow as an attribute name is left out of the element, and the render warns. This starts in 0.7.3 with no warning release first, because such a key never gave one valid attribute. M003 changes the IP1 text to name both exceptions.
**Consequences:** Letting a user `src` win was rejected, because the first argument would then be ignored. A warning release before the skip was rejected, because it keeps broken markup one release longer and protects no working output.

### D-004 (2026-10-24): Reword GP5 to state user ARIA precedence

**Context:** GP5 says an icon without `label` is `aria-hidden` and a labeled icon gets `role="img"` and `aria-label`. Since M001 (0.7.2), a user `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` in any letter case turns the `aria-hidden` default off, and a user `role` or `aria-label` replaces the one that `label` adds (IP1). The GP5 text no longer matches the behavior.
**Decision:** The user chose at the M005 plan gate to reword GP5 so that it names these exceptions. M005 changes the GP5 text. The behavior does not change.
**Consequences:** Keeping GP5 as written was rejected, because it states a default that IP1 already overrides. An icon that a user `role="img"` leaves with no name gets a render warning from M005 (GP2), not a changed default.

### D-005 (2026-10-25): An empty first argument gives no element (narrows IP1 and IP5)

**Context:** A `li` or `lif` call whose first argument is empty, such as `{{< li "" >}}`, made a `<lord-icon>` with `src="https://cdn.lordicon.com/.json"` or `src=""` and gave no warning. The CDN has no such file. IP1 says every user attribute reaches `<lord-icon>` unchanged. IP5 asks for one warning release before the passthrough meaning breaks.
**Decision:** The user chose at the M011 plan gate that such a call makes no element and gives a render warning in HTML output, as a call with no first argument does since 0.7.9. At the M011 escalation offer the user chose to record this as an exception to IP1: the call's other keys reach no element. It starts in 0.7.10 with no warning release first, because such a call never loaded an icon. M011 changes the IP1 and IP5 text to name it.
**Consequences:** Keeping the element and adding a warning was rejected, because the element can never load an icon. This entry does not cover the no-element result of a call with no first argument; the candidate row "Decide whether IP1 names Quarto's drops" holds that question.

### D-006 (2026-10-26): Skip keys that hold `<` or a noncharacter (narrows IP1 and IP5; extends D-003)

**Context:** D-003 skips a key that HTML does not allow as an attribute name, but its set missed two kinds of key. HTML forbids the 66 Unicode noncharacters in an attribute name (whatwg-html §13.1.2.3, whatwg-infra §4.6). The same rule allows `<`, but parsers report a `<` in a name as a parse error and keep it in the name (whatwg-html §13.2.2). Both kinds reached `<lord-icon>` unchanged.
**Decision:** The user chose at the M012 plan gate to skip both kinds of key with the invalid-name warning, and at the M012 escalation offer to write this text without a Fable review. It starts in 0.7.11 with no warning release first. D-003's reason does not hold for `<`, because a key such as `a<b` did give an attribute. The reason here is that no `<lord-icon>` attribute has a name that holds `<` or a noncharacter, so the skip breaks no icon. M012 changes the IP1 and IP5 text.
**Consequences:** Skipping only noncharacters was rejected, because the spec says a `<` in a name can be a sign of a typo. The warning is IP1's warning about a skipped key, not a GP2 guardrail, because no icon fails here.

### D-007 (2026-10-26): A call with no first argument gives no element, and Quarto's drops are not exceptions (narrows IP1; extends D-005)

**Context:** Since 0.7.9 a `li` or `lif` call with no first argument makes no element and, in HTML output, warns. Before 0.7.9 such a call stopped the render with an error. IP1 named only an empty first argument (D-005), and D-005's Consequences left the missing argument to the candidate row "Decide whether IP1 names Quarto's drops". Quarto also drops a quoted value or positional argument that starts with a space or tab before the extension runs, and IP1 did not say whether that is an exception.
**Decision:** The user chose at the M013 plan gate to name both cases in IP1. A call whose first argument is missing joins a call whose first argument is empty: it makes no element, so its keys reach none, and the render warns. A value or positional argument that Quarto drops before the extension runs never reaches the extension, so it is outside IP1 and not one of its exceptions. IP5 does not change, because a call with no first argument stopped the render before 0.7.9, so the no-element result broke no working output.
**Consequences:** Naming only the missing argument was rejected, because IP1 would then read as if the extension forwards values that Quarto drops. Leaving IP1 as written was rejected, because it did not match the behavior since 0.7.9. README already documents Quarto's drops, so no user doc changes.
