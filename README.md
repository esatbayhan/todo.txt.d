# todo.txt.d format

A complete primer on the whys and hows of todo.txt.d.

> This is a fork of the original [todo.txt specification](https://github.com/todotxt/todo.txt), adapted to be Syncthing-friendly. The task syntax remains identical to todo.txt. The key change is the storage model: instead of a single `todo.txt` file, tasks are stored as individual files inside a `todo.txt.d/` directory. This eliminates most sync conflicts when using file-based synchronization tools like [Syncthing](https://syncthing.net/), because independent changes on different devices touch different files.

The first and most important rule of todo.txt.d:

> Tasks are stored as `.txt` files in your `todo.txt.d/` directory.

It is recommended that each file contains a single task for maximum sync-friendliness. A file may also contain multiple tasks (one per line). See [Storage Format](#storage-format) for details.


## Why plain text?

Plain text is software and operating system agnostic. It's searchable, portable, lightweight, and easily manipulated. It's unstructured. It works when someone else's web server is down or your Outlook .PST file is corrupt. There's no exporting and importing, no databases or tags or flags or stars or prioritizing or _insert company name here_-induced rules on what you can and can't do with it.

Tasks can be created and read with any plain text editor - no special tools required. This is a core principle inherited from todo.txt.


## Why a directory?

When multiple devices edit the same `todo.txt` file independently, file-based sync tools like Syncthing produce conflicts - even when the changes are completely unrelated (e.g., adding different tasks on different devices).

By storing each task as its own file inside a `todo.txt.d/` directory, independent changes touch different files. Syncthing syncs them without conflict. The only remaining conflict scenario is editing the *same* task on two devices simultaneously, which is far less common.


## The 3 axes of an effective todo list

Using special notation in todo.txt.d, you can create a list that's sliceable by 3 key axes.


### Priority
Your todo list should be able to tell you what's the next most important thing for you to get done - either by project or by context or overall. You can optionally assign tasks a priority that'll bubble them up to the top of the list.


### Project
The only way to move a big project forward is to tackle a small subtask associated with it. Your todo list should be able to list out all the tasks specific to a project.

In order to move along a project like "Cleaning out the garage," my task list should give me the next logical action to take in order to move that project along. "Clean out the garage" isn't a good todo item; but "Call Goodwill to schedule pickup" in the "Clean out garage" project is.


### Context
[Getting Things Done](https://en.wikipedia.org/wiki/Getting_Things_Done) author David Allen suggests splitting up your task lists by context - ie, the place and situation where you'll work on the job. Messages that you need to send go in the `@email` context; calls to be made `@phone`, household projects `@home`.

That way, when you've got a few minutes in the car with your cell phone, you can easily check your `@phone` tasks and make a call or two while you have the opportunity.

This is all possible inside todo.txt.d.


## Task format rules

<img src="./description.svg" width="100%" height="500">

Each task in todo.txt.d is a single line of plain text. The task syntax is identical to the [original todo.txt format](https://github.com/todotxt/todo.txt). To take advantage of structured task metadata like priority, projects, context, creation, and completion date, there are a few simple but flexible format rules.

Philosophically, the todo.txt.d format has two goals:

- The file contents should be human-readable without requiring any tools other than a plain text viewer or editor.
- A user can manipulate the file contents in a plain text editor in sensible, expected ways. For example, a text editor that can sort lines alphabetically should be able to sort your task list in a meaningful way.

These two goals are why, for example, lines start with priority and/or dates, so that they are easily sorted by priority or time, and completed items are marked with an `x`, which both sorts at the bottom of an alphabetical list and looks like a filled-in checkbox.

Here are the rest.


## Incomplete Tasks: 3 Format Rules

The beauty of todo.txt.d is that it's completely unstructured; the fields you can attach to each task are only limited by your imagination. To get started, use special notation to indicate task context (e.g. `@phone` ), project (e.g. `+GarageSale` ) and priority (e.g. `(A)` ).

A todo.txt.d directory might contain a file with:

```
(A) Thank Mom for the meatballs @phone
```

And another file with:

```
(B) Schedule Goodwill pickup +GarageSale @phone
```

A search and filter for the `@phone` contextual items would output:

```
(A) Thank Mom for the meatballs @phone
(B) Schedule Goodwill pickup +GarageSale @phone
```

To just see the `+GarageSale` project items would output:

```
(B) Schedule Goodwill pickup +GarageSale @phone
Post signs around the neighborhood +GarageSale
```

There are three formatting rules for current tasks.

### Rule 1: If priority exists, it ALWAYS appears first.

The priority is an uppercase character from A-Z enclosed in parentheses and followed by a space.

This task has a priority:

```
(A) Call Mom
```

These tasks do not have any priorities:

```
Really gotta call Mom (A) @phone @someday
(b) Get back to the boss
(B)->Submit TPS report
```


### Rule 2: A task's creation date may optionally appear directly after priority and a space.

If there is no priority, the creation date appears first. If the creation date exists, it should be in the format `YYYY-MM-DD`.

These tasks have creation dates:

```
2011-03-02 Document +TodoTxt task format
(A) 2011-03-02 Call Mom
```

This task doesn't have a creation date:

```
(A) Call Mom 2011-03-02
```


### Rule 3: Contexts and Projects may appear anywhere in the line _after_ priority/prepended date.

- A *context* is preceded by a single space and an at-sign (`@`).
- A *project* is preceded by a single space and a plus-sign (`+`).
- A *project* or *context* token may also appear at the very start of a task's description, without a preceding space.
- A *project* or *context* contains any non-whitespace character.
- A *task* may have zero, one, or more than one *projects* and *contexts* included in it.

For example, this task is part of the `+Family` and `+PeaceLoveAndHappiness` projects as well as the `@iphone` and `@phone` contexts:

```
(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone
```

This task has no contexts in it:

```
Email SoAndSo at soandso@example.com
```

This task has no projects in it:

```
Learn how to add 2+2
```



## Complete Tasks: 2 Format Rules

Two things indicate that a task has been completed.


### Rule 1: A completed task starts with a lowercase x character (`x`).

If a task starts with an `x` (case-sensitive and lowercase) followed directly by a space, it is marked as complete.

This is a complete task:

```
x 2011-03-03 Call Mom
```

These are not complete tasks.

```
xylophone lesson
X 2012-01-01 Make resolutions
(A) x Find ticket prices
```

We use a lowercase x so that completed tasks sort to the bottom of the task list using standard sort tools.


### Rule 2: The date of completion appears directly after the x, separated by a space.

For example:

```
x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github
```

If you've prepended the creation date to your task, on completion it will appear directly after the completion date. This is so your completed tasks sort by date using standard sort tools. Many todo.txt.d clients discard priority on task completion. To preserve it, use the `key:value` format described below (e.g. `pri:A`)

With the completed date (required), if you've used the prepended date (optional), you can calculate how many days it took to complete a task.



## Additional File Format Definitions

Tool developers may define additional formatting rules for extra metadata.

Developers should use the format `key:value` to define additional metadata (e.g. `due:2010-01-02` as a due date).

Both `key` and `value` must consist of non-whitespace characters, which are not colons. Only one colon separates the `key` and `value`.


### Date keys

The following date keys are defined by this specification. All date values **must** use the `YYYY-MM-DD` format. Relative or human-readable values (e.g. `today`, `next week`, `tomorrow`) are not valid — implementations must not accept or produce them.

#### `due:YYYY-MM-DD`

The deadline for the task — it should be completed no later than this date.

```
(A) 2024-01-15 Submit tax return due:2024-04-15
```

#### `scheduled:YYYY-MM-DD`

The date on which the task is scheduled.

```
2024-03-01 Prepare quarterly report scheduled:2024-03-20 due:2024-03-31
```

#### `starting:YYYY-MM-DD`

The earliest date on which the task becomes relevant or actionable.

```
Buy birthday gift for Alice starting:2024-06-01 due:2024-06-10
```

## Storage Format

The storage format is what distinguishes todo.txt.d from the original todo.txt specification.

### The `todo.txt.d/` directory

Tasks are stored as `.txt` files inside a `todo.txt.d/` directory.

```
todo.txt.d/
|-- call-mom.txt
|-- buy-groceries.txt
|-- schedule-pickup.txt
|-- lists.d/
|   |-- today.list
|   +-- inbox.list
+-- done.txt.d/
    |-- fix-bike.txt
    +-- pay-bills.txt
```

### File content

Each `.txt` file contains one or more tasks, one task per line, using the task format rules described above.

**Recommended**: One task per file. This maximizes the sync benefit - each task is an independent file that can be added, modified, or deleted without affecting other tasks.

**Allowed**: Multiple tasks per file (one per line). A traditional `todo.txt` file placed inside the directory is valid. However, this does not provide the sync conflict-reduction benefit, since multiple devices editing the same multi-task file will still conflict.

### File naming

Any unique filename with a `.txt` extension is valid.

When creating tasks manually with a text editor, any descriptive name works:

```
call-mom.txt
buy-groceries.txt
schedule-goodwill-pickup.txt
```

The filename is arbitrary — use whatever naming scheme suits your workflow.

### The `done.txt.d/` subdirectory

Completed tasks are moved from `todo.txt.d/` to `todo.txt.d/done.txt.d/`.

- The file retains its original filename.
- The task content is updated with the `x` completion marker and completion date, following the complete task format rules above.
- This keeps the active task directory lean and focused on open tasks.
- `done.txt.d/` is nested inside `todo.txt.d/` so that there is a single root directory to sync and to grant application permissions to.

### Deleting a task

To delete a task, simply delete the file. If the file contains multiple tasks, remove the corresponding line.

## Smart Lists

Smart lists are user-defined filter views stored as `.list` files in a `lists.d/` subdirectory. They allow you to define filtered views of your tasks — like "Today", "Inbox", or "Upcoming" — that work consistently across all frontends and devices.

Each `.list` file has a small header (name, icon, sort order) and a filter body:

~~~
---
name: Today
icon: 📅
order: 1
---
due <= today
OR
scheduled <= today

sort by priority desc
sort by due asc
~~~

Filter lines within a block are AND'd together. Blocks separated by `OR` are OR'd. This gives you flexible filtering with a format that's trivial to parse.

Date comparisons support relative offsets: `today + 7` means "7 days from now", `today - 14` means "14 days ago".

See `LISTS.md` for the complete filter format specification.

