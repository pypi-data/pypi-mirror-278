# Tree Maker CLI

A command-line tool to generate a tree structure of a folder and its contents, useful for when you need to add context to your GPT prompts.

## Usage

### Installation

Install via `pip`:

```sh
pip install tree_maker_cli
```

### Using this tool

Once installed, you can call the tool with the command

```sh
tree-maker [arguments]
```

If called without arguments, it will print the tree structure from the current folder. If called with a valid folder path, it will print the tree structure from that location.

```sh
tree-maker /path/to/folder
```

#### Arguments

The following arguments are available:
 + `--depth`: Sets the depth of the tree structure to print
 + `--clipboard` (or `-c`): Copy the tree to the clipboard
 + `--output` (or `-o`): Set the output file path
 + `--exclude`: Files and/or folders to exclude from the tree
 + `--show-hidden`: Show hidden files in the tree structure

For example, to print a tree of depth two with hidden files and excluding the folders `public`, `tmp`, and `log` and then copy it to the clipboard:

```sh
tree-maker --depth=2 -c --show-hidden /path/to/your/app --exclude public tmp log
```

To save to a text file:

```sh
tree-maker [arguments] --output path/to/output.txt
```

