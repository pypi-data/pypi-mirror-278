# reqs-diff


`reqs-diff` is a tool to compare multiple `requirements.txt` files and highlight the differences.

## Installation

```sh
pip install reqs-diff
```

## Usage

Compare requirements files:

```sh
reqs-diff path/to/requirements1.txt path/to/requirements2.txt
```

Only show packages with differing versions:

```sh
reqs-diff path/to/requirements1.txt path/to/requirements2.txt --only-diff
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
