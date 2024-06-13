
# Find and Replace Template Commit Check

This Python package provides a pre-commit hook that finds strings in files and replaces them with other strings.

## Installation

This is an easy to use package which is already available here https://pypi.org/project/find-and-replace-template-commit-check/:

![package to use](./images/pypi-package.png "Title")

You can install the package via pip:

```bash
pip install find-and-replace-template-commit-check
```


## Usage
To use this package, you need to add it to your pre-commit configuration file (.pre-commit-config.yaml). Here's an example:

```
repos:
  - repo: local
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

In this configuration, the find-and-replace hook is set to read search and replacement strings from a file (.project-properties.json by default which should be defined in the root of the project you want to use this package). You can also specify the search and replacement strings directly in the args field (which is not a suggested way).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the terms of the MIT license.

## Building and Publishing

To build and publish it to pypi run
```
bash scripts/publish.sh
```


## Run tests

```
python3 -m unittest tests/test_main.py

```
