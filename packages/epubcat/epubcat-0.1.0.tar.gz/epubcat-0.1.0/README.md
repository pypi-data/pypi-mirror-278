# epubcat

[![PyPI - Version](https://img.shields.io/pypi/v/epubcat.svg)](https://pypi.org/project/epubcat)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/epubcat.svg)](https://pypi.org/project/epubcat)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install epubcat
```

## Usage

```command
usage: epubcat [-h] --input INPUT

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
```

Single file

This will take in any file and attempt to read it. It assumes user choose the right file.
```command
epubcat -i /path/to/some/file.epub
```

Globbed file

This will glob any file (including non-epubs!) that matches.
```command
epubcat -i /path/to/some/file*.epub
```

*Directory of files*

This will recursively glob the directory for any epub files.
```command
epubcat -i /path/to/some/dir/
```

## Knonwn Sources of Error

* This uses FTFY to attempt to fix wonky encodings. It can and will do bad things to your output and just continue on. 

## License

`epubcat` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
