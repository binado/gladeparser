import os

import pytest
import numpy as np
from pandas import read_hdf

from gladeparser.parser import to_df, to_hdf5
from gladeparser.columns import Group
from .fixtures import *

class TestParse:
    def test_parse_to_df(self, filename, descriptor):
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

    def test_parse_to_hdf5(self, filename, descriptor):
        indices = [
            Group.ID.value,
            Group.CATALOG_ID.value
        ]
        cols = descriptor.get_columns(*indices, names=True)
        dirname = os.getcwd()
        outfile = os.path.join(dirname, 'out.hdf5')
        hdf5_key = 'test_key'
        to_hdf5(filename, outfile, hdf5_key, cols)

        assert os.path.isfile(outfile)

        # Read data
        df = read_hdf(outfile, hdf5_key)

        assert df is not None
        assert df.columns.to_list() == cols
        assert len(df) == 50

        last_line = df.iloc[-1]
        assert last_line['GLADE no'] == 50
        assert np.isnan(last_line['PGC no'])
        assert np.isnan(last_line['GWGC name'])
        assert np.isnan(last_line['HyperLEDA name'])

        os.remove(outfile)
        assert not os.path.isfile(outfile)

