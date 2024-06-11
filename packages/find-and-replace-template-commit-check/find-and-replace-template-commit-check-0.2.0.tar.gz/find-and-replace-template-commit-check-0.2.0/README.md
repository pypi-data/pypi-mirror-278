<!-- # ${PROJECT_NAME}

## Description

${PROJECT_DESCRIPTION_SLUG}

This project is part of the ${BUSINESS_UNIT}.

The code is hosted at ${GITHUB_REPO_URL}.
${PROJECT_NAME}
## Contributors

${PROJECT_CONTRIBUTORS}

## Repository

This repository is managed by the tucowsinc/iaascloudenablement team.

## Edge Cases

Here are some edge cases to test:

- A string with a backslash: `\\\\`
- A string with a newline character: `\\\\n`
- A string with a tab character: `\\\\t` -->

# Find and Replace Template Commit Check

This Python package provides a pre-commit hook that finds strings in files and replaces them with other strings.

## Installation

You can install the package via pip:

```bash
pip install find-and-replace-template-commit-check

Usage
To use this package, you need to add it to your pre-commit configuration file (.pre-commit-config.yaml). Here's an example:

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

In this configuration, the find-and-replace hook is set to read search and replacement strings from a file (.project-properties.json by default). You can also specify the search and replacement strings directly in the args field.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the terms of the MIT license.

```

