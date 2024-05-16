import pytest

import numpy as np

from gladeparser.columns import Group
from .fixtures import *

class TestColumn:
    def test_column_names(self, columns, column_names):
        ids = [1, 2, 3, 4, 5, 6, 7, 8]
        names = [
            'GLADE no',
            'PGC no',
            'GWGC name',
            'HyperLEDA name',
            '2MASS name',
            'WISExSCOS name',
            'SDSS-DR16Q name',
            'Object type flag'
        ]

        assert columns.names(ids) == names

        # All
        assert columns.names() == column_names

    def test_dtypes(self, columns):
        true_dtypes = [int] + [str] * 7 + [np.float64] * 32
        dtypes = list(columns.dtypes.values())
        assert true_dtypes == dtypes

    def test_get(self, columns, column_names):
        identifier_ids = [2, 3, 4, 5, 6, 7]

        # Direct ID
        args = identifier_ids
        ids = columns.get(*args)
        assert ids == identifier_ids

        # ID per group
        args = [Group.CATALOG_ID.value]
        ids = columns.get(*args)
        assert ids == identifier_ids

        # ID per column name
        args = [
            'PGC no',
            'GWGC name',
            'HyperLEDA name',
            '2MASS name',
            'WISExSCOS name',
            'SDSS-DR16Q name'
        ]
        ids = columns.get(*args)
        assert ids == identifier_ids
        names = columns.get(*args, names=True)
        assert names == args

        # Repeated ids
        args = identifier_ids + [Group.CATALOG_ID.value]
        ids = columns.get(*args)
        assert ids == identifier_ids

        # All rows
        names = columns.get(names=True)
        assert names == column_names

        
