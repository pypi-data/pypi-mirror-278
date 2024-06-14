# find-and-replace

Python package and pre-commit-hook for finding and replacing string(s) in file(s).

## Installation

This is an easy to use package which is already available here https://pypi.org/project/find-and-replace-template-commit-check/:

![package to use](./assets/pypi-package.png "Title")

You can install the package via pip:

```bash
pip install find-and-replace-template-commit-check
```

## Usage

To use this package, you need to add it to your pre-commit configuration file (.pre-commit-config.yaml). Here's an example:

```
repos:
  - repo: https://github.com/andreouellet/pre-commit-find-and-replace-test (To be changed when repo is ready)
    rev: test3
    hooks:
    - id: find-and-replace
      name: find-and-replace
      description: Find and replace strings
      entry: find-and-replace
      language: python
      pass_filenames: true
      exclude_types:
        - binary
      args: ["--read-from-file", "true"]
      files: README.md
      verbose: true

```

Please note you also have a choice of
      files: '.*\.md$'
or
      files: .

In this configuration, the find-and-replace hook is set to read search and replacement strings from a file (.project-properties.json by default which should be defined in the root of the project you want to use this package). You can also specify the search and replacement strings directly in the args field (which is not a suggested way).


## Run tests

```
python -m unittest tests.test_main

```

## How to run it using installed python package

```
  pip install find-and-replace-template-commit-check
   find-and-replace --config .find-and-replace.json README1.md README2.md
```


## If you need more help with the flags and usage of them

```
find-and-replace -h
usage: find-and-replace [-h] [--search SEARCH] [--replacement REPLACEMENT] [--read-from-file READ_FROM_FILE]
                        [--config REPLACEMENTS_FILE]
                        [files ...]

This script performs search and replace operations on one or more files. It supports two modes of operation: Direct Mode and
File Mode. In Direct Mode, you specify the search and replacement strings directly on the command line. In File Mode, the script
reads the search and replacement strings from a JSON file.

positional arguments:
  files                 Files to perform search and replace

options:
  -h, --help            show this help message and exit
  --search SEARCH       Text to search for
  --replacement REPLACEMENT
                        Text to replace with
  --read-from-file READ_FROM_FILE
                        Read search and replacement strings from file
  --config REPLACEMENTS_FILE
                        Path to the replacements file

```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the MIT license.

## Building and Publishing

To build and publish it to pypi run

```
bash scripts/publish.sh
```

## Reference Info

* https://www.gnu.org/prep/standards/html_node/Option-Table.html#Option-Table
* https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
* https://packaging.python.org/guides/distributing-packages-using-setuptools/
* https://autopilot-docs.readthedocs.io/en/latest/license_list.html
* https://pypi.org/classifiers/
