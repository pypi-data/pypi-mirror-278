import os
import argparse

DEFAULT_EXCLUDED_FILES = [
    '__pycache__', 'venv', 'node_modules', 'dist', 'build', 'static', 'media'
]

def is_hidden(item):
    return item.startswith('.')

def generate_tree(folder, depth, show_hidden, prefix='', excluded_files=None):
    if excluded_files is None:
        excluded_files = []

    excluded_files.extend(DEFAULT_EXCLUDED_FILES)

    folders = []
    files = []

    for item in os.listdir(folder):
        if item in excluded_files or (not show_hidden and is_hidden(item)):
            continue

        if os.path.isdir(os.path.join(folder, item)):
            folders.append(item)
        else:
            files.append(item)

    folders.sort()
    files.sort()

    tree = ''

    for item in folders:
        is_last = item == folders[-1] and not files

        if prefix == '':
            tree += '├── '
            new_prefix = '│   '
        else:
            if is_last:
                tree += prefix + '└── '
                new_prefix = prefix + '    '
            else:
                tree += prefix + '├── '
                new_prefix = prefix + '│   '

        tree += item + '/\n'

        if depth is None or depth > 0:
            tree += generate_tree(os.path.join(folder, item), depth - 1 if depth is not None else None, show_hidden, new_prefix, excluded_files)

    for item in files:
        is_last = item == files[-1]

        if prefix == '':
            tree += '├── '
        else:
            if is_last:
                tree += prefix + '└── '
            else:
                tree += prefix + '├── '

        tree += item + '\n'

    return tree

def main():
    parser = argparse.ArgumentParser(description='Generate a tree structure of a folder.')
    parser.add_argument('folder_path', metavar='folder_path', type=str, nargs='?', default='.', help='Path to the folder for generating the tree structure (default: current folder)')
    parser.add_argument('--depth', type=int, help='Maximum depth of the tree structure (default: unlimited)')
    parser.add_argument('--exclude', nargs='*', default=[], help='Additional files to exclude from the tree structure')
    parser.add_argument('--show-hidden', action='store_true', help='Show hidden files in the tree structure')
    parser.add_argument('--output', '-o', type=str, help='Output file path')
    parser.add_argument('--clipboard', '-c', action='store_true', help='Copy the tree to the clipboard')

    args = parser.parse_args()

    folder_path = args.folder_path
    depth = args.depth
    excluded_files = args.exclude
    show_hidden = args.show_hidden

    tree_structure = generate_tree(folder_path, depth, show_hidden, excluded_files=excluded_files)
    root_folder_name = os.path.basename(os.path.abspath(folder_path))

    output = f"{root_folder_name}\n{tree_structure}"

    if args.output:
        with open(args.output, 'w') as file:
            file.write(output)
        print(f"Tree saved to {args.output}")
    elif args.clipboard:
        import pyperclip
        pyperclip.copy(output)
        print("Tree copied to the clipboard")
    else:
        print(output)

if __name__ == '__main__':
    main()
