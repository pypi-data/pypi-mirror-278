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
    parser = argparse.ArgumentParser(description="This script performs search and replace operations on one or more files. It supports two modes of operation: Direct Mode and File Mode. In Direct Mode, you specify the search and replacement strings directly on the command line. In File Mode, the script reads the search and replacement strings from a JSON file.")
    parser.add_argument('files', nargs='*', help='Files to perform search and replace')
    parser.add_argument('--find', help='Text to find in files')
    parser.add_argument('--replacement', help='Text to replace with in files')
    parser.add_argument('--read-from-file', type=bool, default=True, help='Read search and replacement strings from file')
    parser.add_argument('--config', default='.find-and-replace.json', help='Path to the config file')
    args = parser.parse_args()

    if args.read_from_file:
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
    else:
        for filename in args.files:
            replace_in_file(filename, args.find, args.replacement)

if __name__ == "__main__":
    main()