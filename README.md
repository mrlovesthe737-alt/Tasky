# Tasky

Tasky is a lightweight command-line task tracker. Tasks are saved locally in a `tasks.json` file, making it easy to keep simple to-do lists without external dependencies.

## Installation

Tasky only depends on the Python standard library. Run commands using Python 3.10+:

```bash
python tasky.py --help
```

## Usage

Add a task:

```bash
python tasky.py add "Finish writing documentation"
```

List pending tasks:

```bash
python tasky.py list
```

Include completed tasks in the list:

```bash
python tasky.py list --all
```

Mark a task as complete:

```bash
python tasky.py done 1
```

Delete a task:

```bash
python tasky.py delete 1
```
