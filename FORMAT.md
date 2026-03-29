# todo.txt.d Format Specification

**Version:** 1.0.0

## Grammar

Each line in a `.txt` file is a single task. Blank lines are ignored.
Files must be UTF-8 encoded.

~~~ebnf
file            = { task-line | blank-line } ;
task-line       = complete-task | incomplete-task ;
blank-line      = LF | CRLF ;

complete-task   = "x" SP completion-date SP [ creation-date SP ] [ description ] ;
incomplete-task = [ priority SP ] [ creation-date SP ] [ description ] ;

priority        = "(" LETTER ")" ;
LETTER          = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I"
                | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R"
                | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;

date            = DIGIT DIGIT DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT ;
completion-date = date ;
creation-date   = date ;
DIGIT           = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

description     = non-whitespace { SP | non-whitespace } ;
non-whitespace  = (* any character except SP, TAB, CR, LF *) ;

SP              = " " ;
LF              = "\n" ;   (* U+000A *)
CRLF            = "\r\n" ; (* U+000D U+000A *)
~~~

Tokens within a `description` are extracted using these additional rules:

~~~ebnf
project-token            = ( SP | start-of-description ) "+" non-whitespace+ ;
context-token            = ( SP | start-of-description ) "@" non-whitespace+ ;
tag-token                = ( SP | start-of-description ) tag-key ":" tag-value ;
tag-key                  = non-whitespace-non-colon+ ;
tag-value                = non-whitespace-non-colon+ ;
non-whitespace-non-colon = (* any character except SP, TAB, CR, LF, ":" *) ;
~~~

`start-of-description` is a zero-width position: the `+`, `@`, or tag-key may appear as the very first characters of the `description` field (not preceded by a space).

TAB characters (U+0009) within a task line are treated as whitespace — they delimit tokens but are not valid as the single separator between structured fields.

## Data Model

A parsed task has the following fields:

| Field             | Type                  | Notes |
|-------------------|-----------------------|-------|
| `done`            | bool                  | `true` when line starts with `x ` followed by a valid date |
| `completion_date` | `YYYY-MM-DD` \| null  | Present only when `done` is `true` |
| `priority`        | char `A`–`Z` \| null  | Present only when `done` is `false` |
| `creation_date`   | `YYYY-MM-DD` \| null  | Optional; present in both complete and incomplete tasks |
| `description`     | string                | Full remainder after structured prefix fields, unchanged; always a string (never null); empty string `""` when no description text is present |
| `projects`        | list\<string\>        | `+token` values (without `+`), in order of appearance |
| `contexts`        | list\<string\>        | `@token` values (without `@`), in order of appearance |
| `tags`            | map\<string, string\> | `key:value` pairs; first occurrence of each key only |

All date values use the format `YYYY-MM-DD`.
Date validation (e.g. rejecting month 13) is left to the implementation.

## Field Rules

### done

A task is complete when its first two characters are lowercase `x` followed
by a single space, and the next token is a valid `YYYY-MM-DD` date.
If either condition is not met, the line is parsed as an incomplete task.

~~~
x 2024-01-15 Call Mom      → done: true
X 2024-01-15 Call Mom      → done: false  (uppercase X)
xylophone lesson           → done: false  (x not followed by space)
x Call Mom                 → done: false  (no date after x; parsed as incomplete)
~~~

### completion_date

Appears directly after `x `, before any other field.
Must match `YYYY-MM-DD` exactly.

~~~
x 2024-01-15 Call Mom
  ^^^^^^^^^^
  completion_date = "2024-01-15"

x 2024-01-15 2024-01-10 Call Mom
  ^^^^^^^^^^  ^^^^^^^^^^
  completion   creation
  _date        _date
~~~

If the token after `x ` is not a valid `YYYY-MM-DD` date, the line is parsed as an incomplete task
and `completion_date` is not set (see `done` field rule).

### priority

An uppercase letter A–Z enclosed in parentheses, followed by a single space.
Must appear at the very start of an incomplete task's line.
Not present in complete tasks.

~~~
(A) Call Mom               → priority: 'A'
(Z) Someday maybe          → priority: 'Z'
(b) task                   → not a priority (lowercase); token stays in description
(B)->task                  → not a priority (no space after `)`); token stays in description
task (A) description       → not a priority (not at start of line); token stays in description
~~~

### creation_date

Appears after priority (if any), or at the start of the line (if no priority).
In completed tasks, appears after the completion date.
Must match `YYYY-MM-DD` exactly.

~~~
2024-01-15 Call Mom                      → creation_date: "2024-01-15"
(A) 2024-01-15 Call Mom                  → creation_date: "2024-01-15"
x 2024-01-15 2024-01-10 Review PR        → creation_date: "2024-01-10"
(A) Call Mom 2024-01-15                  → creation_date: null  (wrong position)
(A) 01-15-2024 Call Mom                  → creation_date: null  (wrong format; token stays in description)
~~~

### description

The full remainder of the line after all structured prefix fields have been consumed.
Preserved exactly as-is, including any embedded project, context, and tag tokens.

~~~
(A) Call Mom +Family                       → description: "Call Mom +Family"
(A)                                        → description: ""  (priority only; description is empty)
x 2024-01-15 2024-01-10 Review PR          → description: "Review PR"
~~~

### projects

A `+` character followed by one or more non-whitespace characters,
where the `+` is at the start of the description or preceded by a single space.
The value stored in `projects` excludes the leading `+`.

~~~
Call Mom +Family +PeaceLoveAndHappiness    → projects: ["Family", "PeaceLoveAndHappiness"]
Learn how to add 2+2                       → projects: []  (+ not preceded by space)
~~~

### contexts

An `@` character followed by one or more non-whitespace characters,
where the `@` is at the start of the description or preceded by a single space.
The value stored in `contexts` excludes the leading `@`.

~~~
Call Mom @phone @iphone                    → contexts: ["phone", "iphone"]
Email soandso@example.com                  → contexts: []  (@ preceded by non-space)
~~~

### tags

A token preceded by a space or appearing at the start of the description,
containing exactly one colon, where neither the key (before the colon) nor
the value (after the colon) is empty or contains a colon or whitespace.

~~~
Submit tax return due:2024-04-15           → tags: {"due": "2024-04-15"}
Prepare report scheduled:2024-03-20        → tags: {"scheduled": "2024-03-20"}
Meeting at time:12:30                      → tags: {}  (value "12:30" contains a colon; token stays in description)
~~~

Defined tag keys and their value formats:

| Key         | Value format | Meaning |
|-------------|--------------|---------|
| `due`       | `YYYY-MM-DD` | Deadline — must be completed no later than this date |
| `scheduled` | `YYYY-MM-DD` | Date on which the task is scheduled |
| `starting`  | `YYYY-MM-DD` | Earliest date the task becomes relevant or actionable |

For defined date-value tag keys, if the value does not match `YYYY-MM-DD` exactly,
the token is not parsed as a tag (see Lenient Parsing).

## Parsing Rules

### Lenient Parsing

If any token does not conform to the expected format, it is not parsed as
structured metadata. The token remains in the `description` string unchanged.
Implementations must not throw, return an error, or abort parsing when
encountering malformed input. Within a line, unrecognized tokens are left
in the `description`; parsing of that line continues normally.
Parsing continues to the next line.

| Malformed input              | Behavior |
|------------------------------|----------|
| `due:next-week`              | `due` is a defined date-value key; `next-week` is not `YYYY-MM-DD`; token stays in description |
| `(b) task`                   | prefix `(b)` not a priority; stays in description |
| `x Call Mom`                 | Not a complete task (no date after `x`); parsed as incomplete |
| `(A) 01-15-2024 task`        | `01-15-2024` not a valid date format; token stays in description |
| `X 2024-01-01 task`          | Uppercase `X` not a completion marker; parsed as incomplete |

### Duplicate Keys

If the same tag key appears more than once in a task line, only the first
occurrence is parsed as structured metadata and stored in `tags`.
All subsequent occurrences are not parsed as tags — the token stays in the
`description` string unchanged.

~~~
task due:2024-01-01 due:2024-02-01
     ^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^
     tags["due"]    stays in description as "due:2024-02-01"
     = "2024-01-01"
~~~

The first occurrence takes precedence regardless of whether its value is valid.
A malformed first occurrence (e.g., `due:next-week`) still consumes the key —
a subsequent `due:2024-01-01` on the same line is treated as a duplicate and
stays in the description.

## Storage

### Directory structure

Tasks are stored as `.txt` files in a directory. The directory name is not
defined by this specification; `todo.txt.d` is a common convention.

~~~
todo.txt.d/
├── call-mom.txt
├── buy-groceries.txt
└── done.txt.d/
    └── fix-bike.txt
~~~

`done.txt.d/` is the only subdirectory defined by this specification.
No other subdirectories may be created inside the task directory.

### File content

Each `.txt` file contains one or more tasks, one task per line.
Blank lines are ignored. UTF-8 encoding is required.
One task per file is recommended for maximum sync-friendliness.
Each task line must be terminated by a newline character (LF or CRLF).

### File naming

Any unique filename with a `.txt` extension is valid.
The filename carries no semantic meaning and is not part of the task format.

### The done.txt.d/ subdirectory

Completed tasks are moved from the task directory to a `done.txt.d/` subdirectory.
The file retains its original filename.
The task content is updated with the `x` completion marker and completion date.

### Deleting a task

Delete the file to delete the task.
If the file contains multiple tasks, remove the corresponding line.
