import pytest

import numpy as np

from gladeparser.columns import Group, GLADEDescriptor

from .fixtures import column_names

descriptor = GLADEDescriptor()
cols = column_names()


class TestColumn:
    def test_groups(self):
        table_groups = [g.value for g in Group]
        assert table_groups == descriptor.groups

    def test_column_names(self):
        ids = [1, 2, 3, 4, 5, 6, 7, 8]
        names = [
            "GLADE no",
            "PGC no",
            "GWGC name",
            "HyperLEDA name",
            "2MASS name",
            "WISExSCOS name",
            "SDSS-DR16Q name",
            "Object type flag",
        ]

        assert descriptor._names(ids) == names

        # All
        assert descriptor._names() == cols

    def test_column_dtypes(self):
        true_dtypes = [int] + [str] * 7 + [np.float64] * 32
        dtypes = list(descriptor.column_dtypes.values())
        assert true_dtypes == dtypes

    def test_get(self):
        identifier_ids = [2, 3, 4, 5, 6, 7]

        # Direct ID
        args = identifier_ids
        ids = descriptor.get_columns(*args)
        assert ids == identifier_ids

        # ID per group
        args = [Group.CATALOG_ID.value]
        ids = descriptor.get_columns(*args)
        assert ids == identifier_ids

        # ID per column name
        args = [
            "PGC no",
            "GWGC name",
            "HyperLEDA name",
            "2MASS name",
            "WISExSCOS name",
            "SDSS-DR16Q name",
        ]
        ids = descriptor.get_columns(*args)
        assert ids == identifier_ids
        names = descriptor.get_columns(*args, names=True)
        assert names == args

        # Invalid ids
        with pytest.raises(ValueError):
            descriptor.get_columns(3.14)

        # Repeated ids
        args = identifier_ids + [Group.CATALOG_ID.value]
        ids = descriptor.get_columns(*args)
        assert ids == identifier_ids

        # All rows
        names = descriptor.get_columns(names=True)
        assert names == cols
