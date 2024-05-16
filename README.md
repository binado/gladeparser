# gladeparser

Parser for the GLADE+ galaxy catalog.

## Using the package

```python
gc = GLADEColumns()

# Select the columns you want
cols = gc.names('Localization', 'Distance')

# Parse to a Pandas.DataFrame
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
