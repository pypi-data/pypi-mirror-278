"""
These adapters are turned on by default and require no customization
"""

import datetime as dt
from io import BytesIO
from typing import List

from antipickle.base import AbstractAdapter, wrap


class SetAdapter(AbstractAdapter):
    typestring = "set"

    def check_type(self, obj):
        return type(obj) == set  # noqa: E721

    def to_dict(self, obj):
        return {"data": [wrap(x) for x in obj]}

    def from_dict(self, d):
        return set(d["data"])


class TupleAdapter(AbstractAdapter):
    typestring = "tuple"

    def check_type(self, obj):
        return type(obj) == tuple

    def to_dict(self, obj):
        return {"data": [wrap(x) for x in obj]}

    def from_dict(self, d):
        return tuple(d["data"])


class NumpyAdapter(AbstractAdapter):
    typestring = "np.ndarray"
    package_name = "numpy"

    def check_type(self, obj):
        import numpy as np

        return isinstance(obj, np.ndarray)

    def to_dict(self, obj):
        import numpy as np

        bytes_io = BytesIO()
        np.save(bytes_io, obj, allow_pickle=False, fix_imports=False)
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        import numpy as np

        bytes_io = BytesIO(d["data"])
        return np.load(bytes_io, allow_pickle=False)


class NumpyScalarAdapter(AbstractAdapter):
    typestring = "np.scalar"
    package_name = "numpy"

    def check_type(self, obj):
        import numpy as np

        return isinstance(obj, (np.bool_, np.number))

    def to_dict(self, obj):
        import numpy as np

        bytes_io = BytesIO()
        np.save(bytes_io, np.asarray(obj), allow_pickle=False, fix_imports=False)
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        import numpy as np

        bytes_io = BytesIO(d["data"])
        arr = np.load(bytes_io, allow_pickle=False)
        assert arr.ndim == 0
        return arr[()]


class DateTimeAdapter(AbstractAdapter):
    typestring = "dt.datetime"

    def check_type(self, obj):
        return isinstance(obj, dt.datetime)

    def to_dict(self, obj):
        return {"data": dt.datetime.isoformat(obj)}

    def from_dict(self, d):
        return dt.datetime.fromisoformat(d["data"])


class DateAdapter(AbstractAdapter):
    typestring = "dt.date"

    def check_type(self, obj):
        return isinstance(obj, dt.date)

    def to_dict(self, obj):
        return {"data": dt.date.isoformat(obj)}

    def from_dict(self, d):
        return dt.date.fromisoformat(d["data"])


class TimeAdapter(AbstractAdapter):
    typestring = "dt.time"

    def check_type(self, obj):
        return isinstance(obj, dt.time)

    def to_dict(self, obj):
        return {"data": dt.time.isoformat(obj)}

    def from_dict(self, d):
        return dt.time.fromisoformat(d["data"])


class TimedeltaAdapter(AbstractAdapter):
    typestring = "dt.timedelta"

    def check_type(self, obj):
        return isinstance(obj, dt.timedelta)

    def to_dict(self, obj):
        return {"data": dt.timedelta.total_seconds(obj)}

    def from_dict(self, d):
        return dt.timedelta(seconds=d["data"])


class ComplexAdapter(AbstractAdapter):
    typestring = "complex"

    def check_type(self, obj):
        return isinstance(obj, complex)

    def to_dict(self, obj):
        return {"data": complex.__repr__(obj)}

    def from_dict(self, d):
        return complex(d["data"])


class PandasDataFrameAdapter(AbstractAdapter):
    typestring = "pd.DataFrame"
    package_name = "pandas"

    def check_type(self, obj):
        import pandas as pd

        return isinstance(obj, pd.DataFrame)

    def to_dict(self, obj):
        bytes_io = BytesIO()
        obj.to_parquet(bytes_io, engine="pyarrow")
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        import pandas as pd

        return pd.read_parquet(BytesIO(d["data"]))


class PandasSeriesAdapter(AbstractAdapter):
    typestring = "pd.Series"
    package_name = "pandas"

    def check_type(self, obj):
        import pandas as pd

        return isinstance(obj, pd.Series)

    def to_dict(self, obj):
        # series is converted to DF, then serialized with parquet
        bytes_io = BytesIO()
        obj.to_frame().to_parquet(bytes_io, engine="pyarrow")
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        # read dataframe, then take the first column
        import pandas as pd

        df = pd.read_parquet(BytesIO(d["data"]))
        return df.iloc[:, 0]


class PolarsDataFrameAdapter(AbstractAdapter):
    typestring = "pl.DataFrame"
    package_name = "polars"

    def check_type(self, obj):
        import polars as pl

        return isinstance(obj, pl.DataFrame)

    def to_dict(self, obj):
        bytes_io = BytesIO()
        obj.write_parquet(bytes_io)
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        import polars as pl

        return pl.read_parquet(BytesIO(d["data"]))


class PolarsSeriesAdapter(AbstractAdapter):
    typestring = "pl.Series"
    package_name = "polars"

    def check_type(self, obj):
        import polars as pl

        return isinstance(obj, pl.Series)

    def to_dict(self, obj):
        bytes_io = BytesIO()
        # convert to frame and write to parquet
        obj.to_frame().write_parquet(bytes_io)
        return {"data": bytes_io.getvalue()}

    def from_dict(self, d):
        import polars as pl

        df = pl.read_parquet(BytesIO(d["data"]))
        # read parquet and take the first column of dataframe
        assert df.shape[1] == 1, "more than one column in df. Sounds wrong"
        return df[:, 0]


# deserialization in scipy.sparse still produces matrices, not arrays :(
# there is no point in supporting matrices at this point.

# class ScipySparseAdapter(AbstractAdapter):
#     typestring = 'sc.sparse'
#     package_name = 'scipy.sparse'
#
#     def check_type(self, obj):
#         from scipy import sparse
#         # process only arrays, not matrices as those will be dropped
#         return isinstance(obj, (
#             sparse.csc_array,
#             sparse.csr_array,
#             sparse.coo_array,
#             sparse.lil_array,
#             sparse.dia_array,
#             sparse.dok_array,
#         ))
#
#     def to_dict(self, obj):
#         from scipy.sparse import save_npz
#         b = BytesIO()
#         save_npz(b, obj, compressed=True)
#         return {'data': b.getvalue()}
#
#     def from_dict(self, d):
#         from scipy.sparse import load_npz
#         return load_npz(BytesIO(d['data']))


all_default_adapters: List[AbstractAdapter] = [
    SetAdapter(),
    TupleAdapter(),
    NumpyAdapter(),
    NumpyScalarAdapter(),
    ComplexAdapter(),
    TimeAdapter(),
    TimedeltaAdapter(),
    DateTimeAdapter(),
    DateAdapter(),
    PandasSeriesAdapter(),
    PandasDataFrameAdapter(),
    PolarsDataFrameAdapter(),
    PolarsSeriesAdapter(),
]
