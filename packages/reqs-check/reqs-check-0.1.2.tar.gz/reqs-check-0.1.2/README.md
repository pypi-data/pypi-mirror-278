
# reqs-check

`reqs-check` is a tool to check and compare multiple `requirements.txt` files for Python projects.


## Installation

To install `reqs-check`, use `pip`:

```sh
pip install reqs-check
```

## Usage
```
Usage: 
    reqs-check [-h] [--only-diff] [--find-duplicates] [--lint] F [F ...]

Check and compare multiple requirements.txt files.

Positional arguments:
  F                  Paths to the requirements.txt files

Options:
  -h, --help         show this help message and exit
  --only-diff        Only show packages with differing versions
```

## Examples

Let's consider the following files: 

**requirements1.txt**
```
pandas==1.1.5
numpy==1.19.5
scipy~=1.5.4
matplotlib==3.3.4
```
and 

**requirements2.txt**
```
pandas==1.1.5
numpy==1.19.3
matplotlib==3.2.1
requests>=2.24.0
scipy==1.5.4
```
### Compare requirements files

This command compares two `requirements.txt` files and highlights the differences.

```sh
reqs-check requirements1.txt requirements2.txt
```
**Output:**
```
+----+------------+---------------------+---------------------+
|    | Package    | requirements1.txt   | requirements2.txt   |
+====+============+=====================+=====================+
|  0 | pandas     | ==1.1.5             | ==1.1.5             |
+----+------------+---------------------+---------------------+
|  1 | numpy      | ==1.19.5            | ==1.19.3            |
+----+------------+---------------------+---------------------+
|  2 | scipy      | ~=1.5.4             | ==1.5.4             |
+----+------------+---------------------+---------------------+
|  3 | matplotlib | ==3.3.4             | ==3.2.1             |
+----+------------+---------------------+---------------------+
|  4 | requests   | Not Present         | >=2.24.0            |
+----+------------+---------------------+---------------------+
```
> **Note:** The values are color-coded for better readability in the terminal.

### Filter to show only packages with differing versions

This command compares two `requirements.txt` files and displays only the packages with differing versions.

```sh
reqs-check --only-diff requirements1.txt requirements2.txt 
```
**Output:**
```
+----+------------+---------------------+---------------------+
|    | Package    | requirements1.txt   | requirements2.txt   |
+====+============+=====================+=====================+
|  1 | numpy      | ==1.19.5            | ==1.19.3            |
+----+------------+---------------------+---------------------+
|  2 | scipy      | ~=1.5.4             | ==1.5.4             |
+----+------------+---------------------+---------------------+
|  3 | matplotlib | ==3.3.4             | ==3.2.1             |
+----+------------+---------------------+---------------------+
|  4 | requests   | Not Present         | >=2.24.0            |
+----+------------+---------------------+---------------------+
```
You can see that the output only shows the packages with differing versions, so the first package `pandas` is not displayed.


## Next Steps

We plan to add more features to `reqs-check` to resolve some use cases that we've had to deal with. 

### Planned features

- Support finding of duplicated packages in the requirements files.

- Support linting of requirements files for best practices.

- Support for additional file formats (e.g., `Pipfile`, `pyproject.toml`).

- Support for additional checks (e.g., security vulnerabilities).

- Integration with CI/CD pipelines for automated checks.

- Detailed reports in various formats (e.g., JSON, HTML).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
