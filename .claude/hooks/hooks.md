# Hooks

These are behavioral guidelines Claude follows when this file is loaded into context. They are **not** enforced automatically by the harness — they rely on Claude reading this file and applying the rules voluntarily. To enforce hooks at the harness level, configure them in `.claude/settings.json`.

---

## Active Hooks

### `post-edit-format`

**Trigger:** After editing any `.py`, `.ts`, or `.js` file
**Action:** Remind the user to run the formatter

After editing a source file, append:

> "Run `{{LINT_COMMAND}}` to format and lint."

Do not run the formatter automatically. Remind only.

---

### `pre-delete-guard`

**Trigger:** Before deleting any file
**Action:** Halt and require explicit confirmation

Before deleting any file, stop and say:

> "About to delete `[filename]`. This cannot be undone. Confirm? (yes/no)"

Do not proceed unless the user explicitly confirms. This applies to generated files, test artifacts, and `.gitkeep` placeholders.

---

### `test-on-core-change`

**Trigger:** After editing any file in `src/`
**Action:** Remind the user to run the test suite

After any edit to `src/`, append:

> "Source file changed. Run `{{TEST_COMMAND}}` to verify nothing is broken."

---

### `block-sensitive-dirs`

**Trigger:** Before modifying any file in `src/auth/`, `src/billing/`, `infra/`, or `migrations/`
**Action:** Halt and require explicit approval

Do not proceed. Say:

> "This file is in a sensitive directory (`[path]`). Explicit approval is required before editing. Confirm? (yes/no)"

Only continue after the user explicitly confirms.

---

### `no-secrets-in-code`

**Trigger:** Before writing any string literal that resembles a key, token, password, or credential
**Action:** Replace with an environment variable reference

Do not write the literal value. Write instead:

```python
import os
value = os.environ["VARIABLE_NAME"]
```

or the equivalent for the project's language. Add the variable name to `.env.example`.

---

### `proposal-before-refactor`

**Trigger:** Before renaming files, moving files, changing function signatures, or restructuring modules
**Action:** Write and present a proposal; wait for approval before executing

Read `.claude/skills/refactor-playbook.md` and follow the proposal template. Do not make any structural change until the proposal is explicitly approved.

---

## Hook Override

If a user explicitly overrides a hook, Claude may proceed — but must log the override:

> "Hook `[hook-name]` overridden by user. Proceeding."
