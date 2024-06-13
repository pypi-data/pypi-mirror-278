# todo-client

[![PyPI version](https://badge.fury.io/py/todo-client.svg)](https://badge.fury.io/py/todo-client)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> Simple To-Do List Manager

A simple command-line interface (CLI) application to manage your to-do list.

## Table of Contents

- [todo-client](#todo-client)
    - [Features](#features)
    - [Requirements](#requirements)
    - [Setup](#setup)
    - [Usage](#usage)
        - [Commands](#commands)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Build Instructions](#build-instructions)
        - [Commands](#commands)
    - [Changelog](#changelog)
        - [Updating the Changelog](#updating-the-changelog)
    - [Contributing](#contributing)
    - [License](#license)

## Features

- Add a new task
- Remove a task by index
- Mark a task as done by index
- List all tasks
- Clear all tasks
- Optionally specify the to-do list file
- Enter REPL mode

## Requirements

- Python 3.7+
- `make` utility

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rmkane/todo-cli.git
   cd todo-cli
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   ./install.sh
   ```

## Usage

The CLI supports the following commands:

```bash
todo-cli {add,remove,list,clear,done} [--file FILE] [--repl]
```

### Commands

- **add**: Add a new task
   ```bash
   todo add "Your new task"
   ```

- **remove**: Remove a task by index
   ```bash
   todo remove 1
   ```

- **done**: Mark a task as done by index
   ```bash
   todo done 1
   ```

- **list**: List all tasks
   ```bash
   todo list
   ```

- **clear**: Clear all tasks
   ```bash
   todo clear
   ```

### Optional Arguments

- **--file FILE**: Specify the to-do list file
   ```bash
   todo list --file mytasks.txt
   ```

- **--repl**: Enter REPL (Read-Eval-Print Loop) mode
   ```bash
   todo --repl
   ```

## Installation

To install this package, you can clone the repository using the following command:

```shell
git clone https://github.com/rmkane/packaging_tutorial.git
```

To install from PyPI:

```shell
pip install todo-client
```

To install locally:

```shell
make install   # Install
.venv/bin/todo # Run
```

## Usage

Here are some examples of how to use this package:

```python
from todo_client.example import add_one

print(add_one(1))  # 2
```

## Build Instructions

This project uses a Makefile for managing build tasks. Here are some of the commands you can use:

- `make all`: Default target, sets up the virtual environment and runs the build.
- `make create_venv`: Creates a virtual environment and installs Poetry.
- `make activate`: Activates the virtual environment.
- `make install_deps`: Installs project dependencies using Poetry.
- `make build`: Sets up the virtual environment, installs dependencies, and runs the build.
- `make publish`: Builds the project and uploads it to TestPyPI.
- `make test`: Runs tests using pytest.
- `make format`: Formats code using black.
- `make apidoc`: Generates Sphinx `.rst` files.
- `make docs`: Builds Sphinx documentation.
- `make clean`: Removes build artifacts.
- `make clean_all`: Removes the virtual environment, build artifacts, and `__pycache__` directories.
- `make help`: Shows available make targets.

Remember to run `source .venv/bin/activate` to activate the virtual environment before running the build commands.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for details.

### Updating the Changelog

To update the changelog, please use the following format:

```markdown
## [Unreleased]

### Added

- New features that have been added since the last release

### Changed

- Changes to existing functionality

### Deprecated

- Features that will be removed in upcoming releases

### Removed

- Features that have been removed

### Fixed

- Any bug fixes

### Security

- Any security enhancements
```

## Contributing

We welcome contributions to this project! To contribute:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/yourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/yourFeature`)
5. Create a new [Pull Request](https://github.com/rmkane/packaging_tutorial/pulls)

## License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.
