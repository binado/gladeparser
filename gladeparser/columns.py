import os
from enum import Enum
from typing import Union, List

import numpy as np
import pandas as pd

COLUMNS_FILENAME = "columns.csv"

DTYPES = {
    "ID": int,
    "Catalog ID": str,
    "Object type flag": str,
    "Localization": np.float64,
    "Magnitude": np.float64,
    "Distance": np.float64,
    "Mass": np.float64,
    "Merger rate": np.float64,
}


def get_column_filepath() -> str:
    dirname = os.getcwd()
    return os.path.join(dirname, COLUMNS_FILENAME)


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
        column_filepath = get_column_filepath()
        self._columns = pd.read_csv(column_filepath, index_col="Column ID")

    def __str__(self):
        return str(self._columns)

    @property
    def groups(self) -> List[str]:
        return list(dict.fromkeys(self._columns["Group"]))

    @property
    def names(self) -> List[str]:
        return self._columns["Column Name"].to_list()

    @property
    def column_dtypes(self):
        dtype_list = self._columns["Group"].map(DTYPES)
        return dict(zip(self.names, dtype_list))

    def _index_to_name(self, indices: List[int]) -> List[str]:
        return self._columns["Column Name"][indices].to_list()

    def _parse_column(self, column: Union[int, str]) -> List[int]:
        if isinstance(column, int):
            return [column]
        if not isinstance(column, str):
            raise ValueError("column argument should be int or str")

        query = (
            f'Group == "{column}"'
            if column in Group.values()
            else f'`Column Name` == "{column}"'
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
    return GLADEDescriptor().get_columns(*args)
