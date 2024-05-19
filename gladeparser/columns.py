import os
from enum import Enum

import numpy as np
import pandas as pd

dirname = os.getcwd()
column_filepath = os.path.join(dirname, 'columns.csv')

_dtypes = {
    'ID': int,
    'Catalog ID': str,
    'Object type flag': str,
    'Localization': np.float64,
    'Magnitude': np.float64,
    'Distance': np.float64,
    'Mass': np.float64,
    'Merger rate': np.float64,
}

class Group(str, Enum):
    ID = 'ID'
    CATALOG_ID = 'Catalog ID'
    OBJECT_TYPE_FLAG = 'Object type flag'
    LOCALIZATION = 'Localization'
    MAGNITUDE = 'Magnitude'
    DISTANCE = 'Distance'
    MASS = 'Mass'
    MERGER_RATE = 'Merger rate'

    def dtype(self):
        return _dtypes[self.name]

class GLADEDescriptor:
    def __init__(self):
        self._columns = pd.read_csv(column_filepath, index_col='Column ID')

    def __str__(self):
        return str(self._columns)

    @property
    def groups(self):
        return list(dict.fromkeys(self._columns['Group']))
    
    @property
    def column_dtypes(self):
        dtype_list = self._columns['Group'].map(_dtypes)
        return dict(zip(self._names(), dtype_list))
    
    def _names(self, indices=None):
        names = self._columns['Column Name']
        filtered = names[indices] if indices is not None else names[:]
        return filtered.to_list()
    
    def _get_index(self, column):
        if isinstance(column, int):
            return [column]
        if not isinstance(column, str):
            raise ValueError

        try:
            Group(column)
            query = f'Group == "{column}"'
        except ValueError:
            query = f'`Column Name` == "{column}"'
        return self._columns.query(query).index.to_list()
    
    def get_columns(self, *args, names=False):
        columns = []
        for arg in args:
            columns += self._get_index(arg)
        # Normalize
        if len(columns) == 0:
            indices = None
        else:
            indices = sorted(list(set(columns)))
        return self._names(indices) if names else indices
