# loadtext

[![pytest](https://github.com/ffreemt/loadtext/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/loadtext/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI - Version](https://img.shields.io/pypi/v/loadtext.svg)](https://pypi.org/project/loadtext)

-----

## Installation

```console
pip install loadtext
```

## Use

```python
from loadtext import loadtext

# blank lines removed
string_text = loadtext("filename or filepath")
list_paragraphs = loadtext("filename or filepath", splitlines=True)
# or list_paragraphs = loadtext("filename or filepath", True)
```

## License

`loadtext` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
