# -*- coding: utf-8 -*-
# import os
# import argparse
# import fileinput
# import json
# import sys

# def replace_in_file(filename, search, replacement):
#     with fileinput.FileInput(filename, inplace=True, backup='.test') as file:
#         for line in file:
#             print(line.replace(rf"{search}", rf"{replacement}"), end='')


# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('files', nargs='*', help='Files to perform search and replace')
#     parser.add_argument('--search', help='Text to search for')
#     parser.add_argument('--replacement', help='Text to replace with')
#     parser.add_argument('--read-from-file', type=bool, default=False, help='Read search and replacement strings from file')
#     args = parser.parse_args()

#     if args.read_from_file:
#         # Read .project-properties.json from the current working directory
#         with open(os.path.join(os.getcwd(), '.project-properties.json'), 'r') as f:
#             replacements = json.load(f)
#             for filename in args.files:
#                 for replacement in replacements:
#                     replace_in_file(filename, replacement['search'], replacement['replacement'])
#     else:
#         for filename in args.files:
#             replace_in_file(filename, args.search, args.replacement)

import os
import argparse
import fileinput
import json
import sys

def replace_in_file(filename, search, replacement):
    with fileinput.FileInput(filename, inplace=True, backup='.test') as file:
        for line in file:
            print(line.replace(rf"{search}", rf"{replacement}"), end='')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='Files to perform search and replace')
    parser.add_argument('--search', help='Text to search for')
    parser.add_argument('--replacement', help='Text to replace with')
    parser.add_argument('--read-from-file', type=bool, default=False, help='Read search and replacement strings from file')
    args = parser.parse_args()

    if args.read_from_file:
        try:
            # Read .project-properties.json from the current working directory
            with open(os.path.join(os.getcwd(), '.project-properties.json'), 'r') as f:
                replacements = json.load(f)
        except FileNotFoundError:
            print("Error: .project-properties.json file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: .project-properties.json is not a valid JSON file.")
            sys.exit(1)

        for filename in args.files:
            for replacement in replacements:
                replace_in_file(filename, replacement['search'], replacement['replacement'])
    else:
        for filename in args.files:
            replace_in_file(filename, args.search, args.replacement)

if __name__ == "__main__":
    main()
