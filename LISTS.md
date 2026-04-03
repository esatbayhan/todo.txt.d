# Smart Lists Specification

**Version:** 1.1.0

Smart lists are user-defined filter views stored as `.list` files in
the `lists.d/` subdirectory of a todo.txt.d task directory. Frontends
read these files to populate their sidebar with filtered task lists
that are consistent across all devices and implementations.

This spec is written for two audiences: **users** who want to create
or edit list files by hand, and **AI coding agents** implementing
frontends that need to parse this format. Every rule is explicit and
unambiguous — an agent should be able to produce a correct parser from
this document alone.

## Grammar

~~~ebnf
list-file       = frontmatter-block body ;

frontmatter-block = "---" LF { frontmatter-line } "---" LF ;
frontmatter-line  = key ":" SP value LF ;
key               = non-whitespace-non-colon+ ;
value             = (* any characters until LF *) ;

body            = [ { filter-block OR-separator } filter-block ] ;
OR-separator    = "OR" LF ;

filter-block    = { line } ;
line            = filter-line | directive-line | comment-line | blank-line ;

filter-line     = comparison | existence | done-filter ;
comparison      = field SP comp-operator SP date-value
                | field SP priority-operator SP LETTER
                | field SP text-operator SP text-value ;
existence       = ( "has" | "no" ) SP field ;
done-filter     = "done" | "not done" ;

comp-operator   = "=" | "<" | "<=" | ">" | ">=" ;
priority-operator = "=" | "above" | "below" ;
text-operator   = "includes" | "excludes" ;

date-value      = "today" [ SP? ( "+" | "-" ) SP? INTEGER ] ;
text-value      = non-whitespace { SP | non-whitespace } ;

directive-line  = sort-directive | group-directive ;
sort-directive  = "sort by" SP field [ SP direction ] ;
group-directive = "group by" SP field [ SP direction ] ;
direction       = "asc" | "desc" ;

comment-line    = "#" (* any characters until LF *) ;
blank-line      = LF ;

field           = "due" | "scheduled" | "starting" | "creation_date"
                | "priority" | "project" | "context" | "description"
                | "done" ;

non-whitespace  = (* any character except SP, TAB, CR, LF *) ;

SP              = " " ;
LF              = "\n" ;
line-ending     = LF | CRLF ;
CRLF            = "\r\n" ;
INTEGER         = DIGIT+ ;
DIGIT           = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
LETTER          = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I"
                | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R"
                | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
~~~

Files must be UTF-8 encoded. Parsers must accept both LF and CRLF line
endings. The grammar uses `LF` for brevity; read it as `line-ending`
throughout.

## Frontmatter

The frontmatter block is delimited by `---` on its own line. It contains
simple `key: value` pairs, one per line. No nesting, no arrays, no
quoting rules.

| Key     | Type    | Required | Description |
|---------|---------|----------|-------------|
| `name`  | string  | yes      | Display name shown in the frontend sidebar |
| `icon`  | string  | no       | Emoji or text label for the list |
| `order` | integer | no       | Sort position in sidebar; lower values first |

If `order` is omitted, the frontend may use alphabetical ordering by
`name` or filename.

Unknown frontmatter keys are ignored.

## Boolean Logic

Filter conditions use Disjunctive Normal Form (DNF):

- Consecutive filter lines within a block are **AND**'d — a task must
  match all conditions in the block.
- Blocks separated by a line containing only `OR` are **OR**'d — a task
  must match at least one block.

A task matches the list if **any block** has **all its conditions**
evaluate to true.

~~~
due <= today
OR
scheduled <= today
~~~

Means: `(due <= today) OR (scheduled <= today)`.

~~~
no due
no scheduled
no starting
~~~

Means: `(no due) AND (no scheduled) AND (no starting)`.

## Filter Conditions

### Date fields

| Field           | Comparison operators     | Existence forms                           |
|-----------------|--------------------------|-------------------------------------------|
| `due`           | `=` `<` `<=` `>` `>=`   | `has due`, `no due`                       |
| `scheduled`     | `=` `<` `<=` `>` `>=`   | `has scheduled`, `no scheduled`           |
| `starting`      | `=` `<` `<=` `>` `>=`   | `has starting`, `no starting`             |
| `creation_date` | `=` `<` `<=` `>` `>=`   | `has creation_date`, `no creation_date`   |

Date values use the grammar:

~~~
date_value = "today" [ ( "+" | "-" ) INTEGER ]
~~~

- `today` — the current date at evaluation time.
- `today + 7` — 7 days from now.
- `today - 14` — 14 days ago.

Spaces around `+` and `-` are optional: `today+7` and `today + 7` are
equivalent.

### Priority field

| Field      | Operators            | Value | Existence forms                |
|------------|----------------------|-------|--------------------------------|
| `priority` | `=` `above` `below`  | A–Z   | `has priority`, `no priority`  |

- `priority = A` — exactly priority A.
- `priority above C` — priority A or B (letters before C).
- `priority below C` — priority D through Z (letters after C).

### Text fields

| Field         | Operators              | Value              | Existence forms              |
|---------------|------------------------|--------------------|------------------------------|
| `project`     | `includes` `excludes`  | text (without `+`) | `has project`, `no project`  |
| `context`     | `includes` `excludes`  | text (without `@`) | `has context`, `no context`  |
| `description` | `includes` `excludes`  | text               | —                            |

Text matching is case-insensitive.

### Done field

- `done` — matches completed tasks.
- `not done` — matches incomplete tasks.

If no `done` / `not done` filter is specified, the list defaults to
showing only incomplete tasks (`not done` is implied). Frontends only
scan `todo.txt.d/` (not `done.txt.d/`) unless a `done` condition is
present. When `done` is present, frontends must also scan `done.txt.d/`.

## Directives

Directives control presentation of matched tasks. They are not filter
conditions and do not participate in boolean logic.

### sort by

~~~
sort by field [asc | desc]
~~~

Sorts the result set by the given field. Default direction is `asc`.
Multiple `sort by` lines are allowed; the first has highest precedence.

### group by

~~~
group by field [asc | desc]
~~~

Groups the result set by the given field. Default direction is `asc`.
Multiple `group by` lines are allowed; the first is the primary grouping.

### Sortable and groupable fields

All fields: `due`, `scheduled`, `starting`, `creation_date`, `priority`,
`project`, `context`, `description`, `done`.

Directives are global — they apply to the final result set regardless of
which OR block they appear in. By convention, place directives after all
filter conditions.

## Parsing Algorithm

1. Read the file as UTF-8 text.
2. Split at `---` lines — extract frontmatter block and filter body.
3. Parse frontmatter — split each line at the first `:` for key-value pairs.
4. Split the filter body by `OR` lines — produces an array of blocks.
5. Within each block, classify each non-blank, non-comment line:
   - `sort by` or `group by` prefix → directive.
   - `done` or `not done` → done filter (check before `no` prefix).
   - `has` or `no` prefix → existence filter.
   - Otherwise → comparison filter (split into field, operator, value).
6. Evaluate: a task matches if any block has all its conditions true.
7. Apply directives: sort and group the matched tasks.

## Storage

List definitions are stored in `todo.txt.d/lists.d/`:

~~~
todo.txt.d/
├── call-mom.txt
├── buy-groceries.txt
├── lists.d/
│   ├── today.list
│   ├── inbox.list
│   └── upcoming.list
└── done.txt.d/
    └── fix-bike.txt
~~~

- Files use the `.list` extension.
- Any unique filename with a `.list` extension is valid.
- The filename carries no semantic meaning.

## Lenient Parsing

Consistent with todo.txt.d's lenient parsing philosophy:

- Unknown frontmatter keys are ignored.
- Unrecognized filter lines are ignored (skipped; parsing continues).
- A `.list` file with no valid filter conditions matches no tasks.
- A `.list` file with no frontmatter `name` may use the filename
  (without extension) as the display name.

Implementations must not throw, return an error, or abort when
encountering malformed input in a `.list` file.
