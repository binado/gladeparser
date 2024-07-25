from numpy import float64
from polars import Int8, Int32, Float64, String

COLUMN_NAMES = [
    "GLADE no",
    "PGC no",
    "GWGC name",
    "HyperLEDA name",
    "2MASS name",
    "WISExSCOS name",
    "SDSS-DR16Q name",
    "Object type flag",
    "RA",
    "Dec",
    "B",
    "B_err",
    "B flag",
    "B_Abs",
    "J",
    "J_err",
    "H",
    "H_err",
    "K",
    "K_err",
    "W1",
    "W1_err",
    "W2",
    "W2_err",
    "W1 flag",
    "B_J",
    "B_J err",
    "z_helio",
    "z_cmb",
    "z flag",
    "v_err",
    "z_err",
    "d_L",
    "d_L err",
    "dist flag",
    "M*",
    "M*_err",
    "M* flag",
    "Merger rate",
    "Merger rate error",
]

GROUPS = [
    "ID",
    "Catalog ID",
    "Catalog ID",
    "Catalog ID",
    "Catalog ID",
    "Catalog ID",
    "Catalog ID",
    "Object type flag",
    "Localization",
    "Localization",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Magnitude",
    "Distance",
    "Distance",
    "Distance",
    "Distance",
    "Distance",
    "Distance",
    "Distance",
    "Distance",
    "Mass",
    "Mass",
    "Mass",
    "Merger rate",
    "Merger rate",
]

DTYPES = {
    "ID": int,
    "Catalog ID": str,
    "Object type flag": str,
    "Localization": float64,
    "Magnitude": float64,
    "Distance": float64,
    "Mass": float64,
    "Merger rate": float64,
}

POLARS_DTYPES = {
    "ID": Int32(),
    "Catalog ID": String(),
    "Object type flag": String(),
    "Localization": Float64(),
    "Magnitude": Float64(),
    "Distance": Float64(),
    "Mass": Float64(),
    "Merger rate": Float64(),
}

POLARS_DTYPES_OVERRIDES = {
    "B flag": Int8(),
    "W1 flag": Int8(),
    "z flag": Int8(),
    "dist flag": Int8(),
    "M* flag": Int8(),
}
