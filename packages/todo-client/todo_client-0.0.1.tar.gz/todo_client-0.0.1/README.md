# Example Package

This is a simple example package. You can use
[GitHub-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

This package is designed to provide [describe functionality]. It's perfect for [describe target audience] and can help
you to [describe benefits].

## Table of Contents

- [Example Package](#example-package)
    - [Project Structure](#project-structure)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Setup](#setup)
    - [Build Instructions](#build-instructions)
        - [Commands](#commands)
    - [Changelog](#changelog)
        - [Updating the Changelog](#updating-the-changelog)
    - [Contributing](#contributing)
    - [License](#license)

## Installation

To install this package, you can clone the repository using the following command:

```sh
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

## Setup

Configure the TestPyPI repository and token:

```sh
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi <your-token>
```

On macOS, the file is located at `~/Library/Application\ Support/pypoetry/config.toml`

Source: [_using python-poetry to publish to test.pypi.org_](https://stackoverflow.com/a/72524326/1762224)

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

### Commands

1. **Create Virtual Environment and Install Poetry**:
    ```sh
    make create_venv
    ```

2. **Activate Virtual Environment**:
    ```sh
    make activate
    ```

3. **Install Project Dependencies**:
    ```sh
    make install_deps
    ```

4. **Build the Project**:
    ```sh
    make build
    ```

5. **Publish to TestPyPI**:
    ```sh
    make publish
    ```

6. **Run Tests**:
    ```sh
    make test
    ```

7. **Format Code**:
    ```sh
    make format
    ```

8. **Generate Sphinx .rst Files**:
    ```sh
    make apidoc
    ```

9. **Build Sphinx Documentation**:
    ```sh
    make docs
    ```

10. **Clean Project**:
    ```sh
    make clean
    ```

11. **Clean All Generated Files**:
    ```sh
    make clean_all
    ```

12. **Show Available Make Targets**:
    ```sh
    make help
    ```

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
