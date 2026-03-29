# Format Fixture Examples

This directory contains fixture files for testing todo.txt.d format implementations.

- **`valid/`** — Spec-compliant task files. A conforming parser must parse each file without errors and produce the field values documented below.
- **`edge-cases/`** — Valid inputs that commonly trip up implementations. A conforming parser must handle these correctly per FORMAT.md.
- **`invalid/`** — Inputs that trigger lenient parsing. A conforming parser must not throw or abort — it must apply lenient parsing and return a best-effort result per FORMAT.md "Lenient Parsing" and "Duplicate Keys" sections.

Both `valid/` and `edge-cases/` are spec-compliant directories: they contain only `.txt` files and a `done.txt.d/` subdirectory. `invalid/` contains files with malformed task content that triggers lenient parsing; the directory structure itself is not special.

## File Index

| File | Category | Spec Rule |
|------|----------|-----------|
| `valid/priority-only.txt` | valid | priority: uppercase letter in `(A)` format at start of line, e.g. `(A)` through `(Z)` |
| `valid/creation-date-no-priority.txt` | valid | creation_date: appears at start of line when no priority |
| `valid/priority-and-creation-date.txt` | valid | priority appears directly before creation_date |
| `valid/priority-creation-date-description.txt` | valid | full incomplete task with priority, creation_date, project, context |
| `valid/single-project.txt` | valid | projects: `+token` preceded by a space |
| `valid/single-context.txt` | valid | contexts: `@token` preceded by a space |
| `valid/multiple-projects-and-contexts.txt` | valid | multiple projects and contexts in one task |
| `valid/tag-due.txt` | valid | tags: `due:YYYY-MM-DD` |
| `valid/tag-scheduled.txt` | valid | tags: `scheduled:YYYY-MM-DD` (also contains `due:`) |
| `valid/tag-starting.txt` | valid | tags: `starting:YYYY-MM-DD` (also contains `due:`) |
| `valid/multiple-tags.txt` | valid | multiple defined date tags in one task |
| `valid/no-metadata.txt` | valid | plain description with no structured fields |
| `valid/project-at-start-of-description.txt` | valid | projects: `+token` at the very start of description (no preceding space) |
| `valid/context-at-start-of-description.txt` | valid | contexts: `@token` at the very start of description (no preceding space) |
| `valid/done.txt.d/completed-basic.txt` | valid | done: `x` prefix with date sets `done: true`; no creation_date |
| `valid/done.txt.d/completed-with-both-dates.txt` | valid | done: `x` prefix sets `done: true`; both completion_date and creation_date present |
| `edge-cases/email-contains-at-sign.txt` | edge-case | contexts: `@` preceded by non-space is not a context |
| `edge-cases/plus-sign-in-math.txt` | edge-case | projects: `+` not preceded by space is not a project |
| `edge-cases/priority-z.txt` | edge-case | priority: `Z` is a valid priority (full A–Z range) |
| `edge-cases/description-starts-with-x-not-complete.txt` | edge-case | done: `x` not followed by a space is not a completion marker |
| `edge-cases/time-with-two-colons-not-a-tag.txt` | edge-case | tags: token whose value contains `:` is not a valid tag |
| `edge-cases/duplicate-date-key.txt` | edge-case | duplicate keys: first valid occurrence is parsed; second stays in description |
| `edge-cases/malformed-first-key-blocks-valid-duplicate.txt` | edge-case | duplicate keys: malformed first occurrence consumes the key; subsequent valid-looking occurrence stays in description |
| `edge-cases/done.txt.d/completed-with-metadata.txt` | edge-case | done: completion_date, creation_date, project, context, and tag all present |
| `invalid/priority-lowercase.txt` | invalid | lenient parsing: lowercase `(b)` not parsed as priority; stays in description |
| `invalid/priority-not-at-start.txt` | invalid | lenient parsing: `(A)` not at start of line; not parsed as priority |
| `invalid/due-key-non-date-value.txt` | invalid | lenient parsing: `due` is a defined date-value key; `next-week` is not `YYYY-MM-DD`; token stays in description |
| `invalid/due-key-partial-date.txt` | invalid | lenient parsing: `due:2024-13` does not match `YYYY-MM-DD` pattern; token stays in description |
| `invalid/completion-marker-uppercase.txt` | invalid | lenient parsing: uppercase `X` not a completion marker; parsed as incomplete task |
| `invalid/completion-date-missing.txt` | invalid | lenient parsing: `x` without a date; parsed as incomplete task |
| `invalid/creation-date-wrong-format.txt` | invalid | lenient parsing: `01-15-2024` is not `YYYY-MM-DD` format (year must come first); token stays in description |
| `invalid/malformed-first-due-key-blocks-valid-second.txt` | invalid | lenient parsing + duplicate keys: malformed first `due:` consumes the key; valid-looking second `due:` stays in description |
