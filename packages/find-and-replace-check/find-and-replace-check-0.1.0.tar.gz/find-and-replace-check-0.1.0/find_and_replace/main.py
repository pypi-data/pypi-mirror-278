# -*- coding: utf-8 -*-
import os
import argparse
import fileinput
import json
import sys


def replace_in_file(filename, search, replacement):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(rf"{search}", rf"{replacement}"), end='')


def main():
    parser = argparse.ArgumentParser(
        description="""Perform find and replace operations on one or more target files. 
                    By default, the script reads the search and replacement entries (strings) from a JSON file.
                    You can also specify the search and replacement strings directly as command line args by setting the
                    --find "search_string" and --replacement "replacement_string" argument options."""
    )
    parser.add_argument(
        '--config', default='.find-and-replace.json',
        help='PATH to JSON config file containing find and replacement entries'
    )
    parser.add_argument(
        '--find', dest='direct_mode', action='store_true', help='String to find in files'
    )
    parser.add_argument(
        '--replacement', dest='direct_mode', action='store_true', help='String to replace with in files'
    )
    parser.add_argument(
        'files', nargs='*', help='File(s) on which to perform search and replace'
    )
    args = parser.parse_args()

    if args.direct_mode:
        # Arguments --find and --replacement have been specified - running in direct mode
        for filename in args.files:
            replace_in_file(filename, args.find, args.replacement)
    else:
        # Arguments --find and --replacement have not been specified - running in default config file mode
        try:
            with open(os.path.join(os.getcwd(), args.config), 'r') as f:
                replacements = json.load(f)
        except FileNotFoundError:
            print(f"Error: {args.config} file not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: {args.config} is not a valid JSON file.")
            sys.exit(1)

        for filename in args.files:
            for replacement in replacements:
                replace_in_file(filename, replacement['search'], replacement['replacement'])


if __name__ == "__main__":
    main()
