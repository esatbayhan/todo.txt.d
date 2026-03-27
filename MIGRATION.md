# Migration Guide

This document describes the differences between todo.txt.d and the original [todo.txt specification](https://github.com/todotxt/todo.txt), and how to migrate between the two formats.


## Differences from todo.txt

| Aspect | todo.txt | todo.txt.d |
|--------|----------|------------|
| **Storage** | Single `todo.txt` file | `todo.txt.d/` directory with one `.txt` file per task (recommended) |
| **Task syntax** | One line = one task | Identical — unchanged from todo.txt |
| **Multi-task files** | The entire file is multi-task by design | Allowed but not recommended (reduces sync benefit) |
| **Archival** | Informal (some clients use a `done.txt` file) | Formalized as `todo.txt.d/done.txt.d/` subdirectory |
| **File naming** | N/A (single file) | Flexible; any `.txt` filename is valid |
| **Sync friendliness** | Conflicts when multiple devices edit the file independently | Conflict-free for independent task additions/edits across devices |

### What changed

- **Storage model**: The single `todo.txt` file is replaced by a `todo.txt.d/` directory. Each task is stored as an individual `.txt` file. This is the core change that enables conflict-free syncing.
- **Archival**: Completed tasks are moved to `todo.txt.d/done.txt.d/`, a subdirectory inside the main task directory. This is now a formal part of the specification, whereas todo.txt left archival as an informal convention.
- **File naming convention**: Since tasks are individual files, a naming convention is needed. Any `.txt` filename is valid — the name is arbitrary.

### What stayed the same

- **Task syntax**: The format of each task line is identical to todo.txt. Priority, creation date, contexts, projects, completion markers, completion dates, and `key:value` metadata all work exactly the same way.
- **Plain text philosophy**: Tasks remain human-readable plain text files that can be created and edited with any text editor.


## Migration guide

### From `todo.txt` to `todo.txt.d/`

#### Quick start (preserves the single file)

You can move your existing `todo.txt` directly into a new `todo.txt.d/` directory:

```sh
mkdir -p todo.txt.d
mv todo.txt todo.txt.d/todo.txt
```

This is valid because multi-task files are allowed in todo.txt.d. **However**, this approach does **not** provide the Syncthing conflict-reduction benefit. The same single-file conflict problem remains. To get the full sync advantage, split the file into one task per file (see below).

#### Full migration (one task per file)

Split each line of your `todo.txt` into an individual file inside `todo.txt.d/`. For example, using a shell script:

```sh
mkdir -p todo.txt.d
n=1
while IFS= read -r line; do
    [ -z "$line" ] && continue
    echo "$line" > "todo.txt.d/task-$(printf '%04d' $n).txt"
    n=$((n + 1))
done < todo.txt
```

This creates files like `task-0001.txt`, `task-0002.txt`, etc. The filenames are arbitrary — use whatever naming scheme suits your workflow.

### From `done.txt` to `done.txt.d/`

The same approach applies. Move or split your `done.txt` into `todo.txt.d/done.txt.d/`:

```sh
mkdir -p todo.txt.d/done.txt.d
n=1
while IFS= read -r line; do
    [ -z "$line" ] && continue
    echo "$line" > "todo.txt.d/done.txt.d/done-$(printf '%04d' $n).txt"
    n=$((n + 1))
done < done.txt
```

### From `todo.txt.d/` back to `todo.txt`

To convert back to a single file:

```sh
cat todo.txt.d/*.txt > todo.txt
```

For completed tasks:

```sh
cat todo.txt.d/done.txt.d/*.txt > done.txt
```

### Python migration script

A Python migration script is provided as `migrate.py`. It requires Python 3 and has no external dependencies.

**Convert todo.txt to todo.txt.d/**:

```sh
python3 migrate.py to-d todo.txt
python3 migrate.py to-d todo.txt -d done.txt          # include done.txt
python3 migrate.py to-d todo.txt -o my-tasks.d         # custom output directory
```

**Convert todo.txt.d/ back to todo.txt**:

```sh
python3 migrate.py from-d todo.txt.d
python3 migrate.py from-d todo.txt.d -o my-todo.txt    # custom output file
```

Run `python3 migrate.py -h` for full usage details.
