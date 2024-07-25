from enum import Enum
from typing import Union, List

import pandas as pd
import polars as pl

from .constants import (
    COLUMN_NAMES,
    GROUPS,
    DTYPES,
    POLARS_DTYPES,
    POLARS_DTYPES_OVERRIDES,
)


class Group(str, Enum):
    ID = "ID"
    CATALOG_ID = "Catalog ID"
    OBJECT_TYPE_FLAG = "Object type flag"
    LOCALIZATION = "Localization"
    MAGNITUDE = "Magnitude"
    DISTANCE = "Distance"
    MASS = "Mass"
    MERGER_RATE = "Merger rate"

    def dtype(self):
        return DTYPES[self.name]

    @classmethod
    def values(cls):
        return list(map(lambda g: g.value, cls))


class GLADEDescriptor:
    def __init__(self):
        self.column_names_col = "Column Name"
        self.group_col = "Group"
        data = {self.column_names_col: COLUMN_NAMES, self.group_col: GROUPS}
        self._columns = pd.DataFrame(
            data=data, index=list(range(1, len(COLUMN_NAMES) + 1))
        )

    def __str__(self):
        return str(self._columns)

    @property
    def _column_names(self):
        return self._columns[self.column_names_col]

    @property
    def _column_groups(self):
        return self._columns[self.group_col]

    @property
    def groups(self) -> List[str]:
        return list(dict.fromkeys(self._columns[self.group_col]))

    @property
    def names(self) -> List[str]:
        return self._column_names.to_list()

    @property
    def column_dtypes(self):
        dtype_list = self._column_groups.map(DTYPES)
        return dict(zip(self.names, dtype_list))

    @property
    def polars_schema(self):
        dtype_list = self._column_groups.map(POLARS_DTYPES)
        dtype_dict = dict(zip(self.names, dtype_list))
        dtype_dict.update(**POLARS_DTYPES_OVERRIDES)
        return pl.Schema(dtype_dict)

    def _index_to_name(self, indices: List[int]) -> List[str]:
        return self._column_names[indices].to_list()

    def _parse_column(self, column: Union[int, str]) -> List[int]:
        if isinstance(column, int):
            return [column]
        if not isinstance(column, str):
            raise ValueError("column argument should be int or str")

        query = (
            f'{self.group_col} == "{column}"'
            if column in Group.values()
            else f'`{self.column_names_col}` == "{column}"'
        )
        return self._columns.query(query).index.to_list()

    def _columns_to_indices(self, *args: Union[int, str]) -> List[int]:
        columns_indices = []
        for arg in args:
            columns_indices += self._parse_column(arg)
        # Normalize
        return sorted(list(set(columns_indices)))

    def get_columns(self, *args: Union[int, str]) -> List[str]:
        columns_indices = self._columns_to_indices(*args)
        return (
            self._index_to_name(columns_indices)
            if len(columns_indices) > 0
            else self.names
        )


def get_columns(*args: Union[int, str]) -> List[str]:
    """Parse column identifiers and return subset of GLADE+ column names.

    Parameters
    ----------
    args: int | str:
        List of column identifier. Each entry may be a GLADE+ column id, column name or group.

    Returns
    -------
    list
        List of GLADE+ column names based on selection

    Examples
    --------
    Getting columns by id:

    >>> get_columns(1, 2, 3)
    ['GLADE no', 'PGC no', 'GWGC name']

    Getting columns by name:

    >>> get_columns("z_cmb", "z flag", "v_err", "z_err")
    ['z_cmb', 'z flag', 'v_err', 'z_err']

    Getting columns by group:

    >>> get_columns("Mass")
    ['M*', 'M*_err', 'M* flag']

    Mixed inputs:

    >>> get_columns(1, 2, 3, "z_cmb", "Mass")
    ['GLADE no', 'PGC no', 'GWGC name', 'z_cmb', 'M*', 'M*_err', 'M* flag']
    """
    return GLADEDescriptor().get_columns(*args)
