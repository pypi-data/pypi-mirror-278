# xsh
xsh is a ssh config manager. It helps you to manage your ssh config file. You can add, remove, list, edit, and connect to your ssh hosts easily.

## Installation
```bash
pip install xsh
```

## Usage
Notice that `xsh add` is equivalent to `xsh host add`. And `xsh yourhost` is equivalent to `xsh host connect yourhost`.
```bash
Usage: xsh <command> [args]
Commands:
  init
  key <command> [args]
  host <command> [args]

Usage: xsh key <command> [args]
Commands:
  add <name>
  ls
  rm <name>

Usage: xsh host <command> [args]
Commands:
  add <name> <user@host>
  ls
  connect <name>
  rm <name>
```

## For Maintainers

### Build
```bash
py -m pip install --upgrade build
py -m build
```

```bash
py -m pip install --upgrade twine
twine upload dist/*
```