# pydtl-relativepath

pydtl-relativepath tool from pydtl community can be used to solve many issues that occurs with relative paths and imports from various modules in your complex framework.

[![Tests](https://github.com/python-dev-tools/pydtl-relativepath/actions/workflows/build_and_tests.yml/badge.svg)](https://github.com/python-dev-tools/pydtl-relativepath/actions/workflows/build_and_tests.yml)
[![codecov](https://codecov.io/gh/python-dev-tools/pydtl-relativepath/graph/badge.svg?token=WULZU647T4)](https://codecov.io/gh/python-dev-tools/pydtl-relativepath)
[![Linting](https://github.com/python-dev-tools/pydtl-relativepath/actions/workflows/lint.yml/badge.svg)](https://github.com/python-dev-tools/pydtl-relativepath/actions/workflows/lint.yml)
![Python Version](https://img.shields.io/badge/Python%20Versions-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![OS Support](https://img.shields.io/badge/OS%20Support-Windows%20%7C%20Linux%20%7C%20MacOS-blue)

## 🔍 Features

- **Convert Relative Paths to Absolute**: Easily convert relative paths to absolute paths based on the current working directory or the current file's directory.
- **PathLib Compatibility**: Seamlessly works with PathLib, allowing for modern path manipulations.
- **Customizable Path Construction**: Adjust path construction through parameters like `parent_dir_jump` to navigate through directory structures.
- **Error Handling**: Provides clear error messages for invalid inputs, such as incorrect `relative_type` values or `parent_dir_jump` configurations.

## 🔧 Installation

To install `pydtl-relativepath`, run the following command in your terminal:

```bash
pip install pydtl-relativepath
```

## 💻 Usage Examples

### Convert Path Relative to Working Directory

To convert a path relative to the current working directory into an absolute path:

```python
from pydtl_relativepath import rel2abs, RelativePathType

path = rel2abs("README.md", relative_type=RelativePathType.RELATIVE_TO_WORKING_DIRECTORY)
print(path)  # Outputs the absolute path to README.md
```

### Convert Path Relative to Current File's Directory

To convert a path relative to the current file's directory:

```python
from pydtl_relativepath import rel2abs, RelativePathType

path = rel2abs("..", "README.md", relative_type=RelativePathType.RELATIVE_TO_CURRENT_FILE)
print(path)  # Outputs the absolute path to README.md located one directory up from the current file
```

### Using parent_dir_jump to Navigate Directories

To navigate up or down the directory structure while converting paths:

```python
from pydtl_relativepath import rel2abs, RelativePathType

# Navigate up one directory from the current file's location
path = rel2abs("README.md", relative_type=RelativePathType.RELATIVE_TO_CURRENT_FILE, parent_dir_jump=-1)
print(path)  # Outputs the absolute path to README.md located one directory up
```

### Handling Errors

The package is designed to raise informative errors for invalid inputs:

```python
from pydtl_relativepath import rel2abs, RelativePathType

try:
    path = rel2abs("README.md", relative_type="invalid_type")
except ValueError as e:
    print(e)  # Will print an error message regarding the invalid relative_type
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the package or add new features.

See our [Contribution Guide](CONTRIBUTING.md) for more details.

## 📜 License

pydtl-relativepath is released under the MIT License. See the LICENSE file for more details.
