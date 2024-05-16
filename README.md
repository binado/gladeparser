# gladeparser

Parser for the [GLADE+ galaxy catalog](https://glade.elte.hu/).

## Using the package

To read the catalog into a `pandas.DataFrame`:

```python
from gladeparser.parser import to_df

filename = # path to GLADE+ calataog
df = to_df(filename)
```

To parse only a subset of rows:

```python
from gladeparser.parser import to_df
from gladeparser.columns import GLADEDescriptor

gc = GLADEDescriptor()

# Select the columns you want and return their names
cols = gc.get_columns('Localization', 'Distance', names=True)

filename = # path to GLADE+ calataog
df = to_df(filename, cols)
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
