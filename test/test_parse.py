import pytest

import numpy as np

from gladeparser.parser import to_df
from gladeparser.columns import Group
from .fixtures import *

class TestParse:
    def test_parse(self, filename, descriptor):
        indices = [
            Group.ID.value,
            Group.CATALOG_ID.value
        ]
        cols = descriptor.get_columns(*indices, names=True)
        df = to_df(filename, cols)
        assert df.columns.to_list() == cols
        assert len(df) == 50

        last_line = df.iloc[-1]
        assert last_line['GLADE no'] == 50
        assert np.isnan(last_line['PGC no'])
        assert np.isnan(last_line['GWGC name'])
        assert np.isnan(last_line['HyperLEDA name'])
