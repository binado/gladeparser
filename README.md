# gladeparser

![tests](https://github.com/binado/gladeparser/actions/workflows/test.yml/badge.svg)

Parser for the [GLADE+ galaxy catalog](https://glade.elte.hu/).

## Usage

To read the catalog into a `pandas.DataFrame`:

```python
from gladeparser import to_df

filename = "path/to/catalog"
df = to_df(filename)
```

### Parsing a subset of columns

```python
from gladeparser import to_df, get_columns

# Select the columns you want and return their names
# See more options in get_columns docstring
cols = get_columns('Localization', 'Distance', names=True)

filename = "path/to/catalog"
df = to_df(filename, cols=cols)
```

## Installation

Clone the repo and run

```bash
pip install .
```

## Testing

Make sure that you have `pytest` installed, or run

```bash
pip install .[dev]
```

Then run

```bash
pytest
```

## References

See the GLADE+ paper on [arXiv](https://arxiv.org/abs/2110.06184).
