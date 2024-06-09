import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd
import antipickle
from antipickle.base import MAGIC_KEY


def get_serializers():
    with TemporaryDirectory() as dir:
        fname = Path(dir).joinpath("file")
        fname_gz = Path(dir).joinpath("file.gz")

        def pack_to_file(o):
            antipickle.dump(o, fname)
            return fname

        def unpack_from_file(fname):
            return antipickle.load(fname)

        yield pack_to_file, unpack_from_file

        def pack_to_file_gz(o):
            antipickle.dump(o, fname_gz)
            return fname_gz

        yield pack_to_file_gz, unpack_from_file

        path = Path.home().joinpath(".test_paths_for_antipickle.antipickle")
        if path.exists():
            # use antipickle to test antipickle, what an irony
            paths = antipickle.load(path)

            def pack_to_s3(o):
                result_path = paths["s3_file_antipickle"]
                antipickle.dump(o, result_path)
                return result_path

            yield pack_to_s3, unpack_from_file

            def pack_to_s3_gz(o):
                result_path = paths["s3_file_antipickle_gz"]
                antipickle.dump(o, result_path)
                return result_path

            yield pack_to_s3_gz, unpack_from_file


def test_simple_types():
    now = datetime.datetime.now()

    x = dict(
        a=None,
        b="string",
        c=b"bytes",
        d=12345,
        e=123.456,
        f=["a", "b", "c", b"bytes", True, False],
        g={1, 2, 3},
        h=now,
        i=now.time(),
        j=now.date(),
        k=datetime.timedelta(weeks=3),
        l=(1 + 2.2j),
        m=(1, [2, 3], {4: 5, (6, "string"): {None, now}}),
        # n=[10 ** 30, -10 ** 30] # fails for integers out of 64-bit range
    )

    for serializer, deserializer in get_serializers():
        assert x == deserializer(serializer(x))

        y = {**x, MAGIC_KEY: {MAGIC_KEY: (1, 2)}}
        y = {**y, "123": {**y, 1: (2, y)}}
        assert y == deserializer(serializer(y))

        z = [y]
        assert z == deserializer(serializer(z))

        z = tuple(z)
        assert z == deserializer(serializer(z))


def test_numpy():
    d1 = dict(
        a=np.zeros([1, 2, 3], dtype="uint8"),
        b=np.asarray(["hi"] * 8),
        c=np.arange(100).astype("float32").reshape([2, 5, 10]),
        d=np.bool_(1),
        e=np.float32(15.0),
        # f=np.float64(15.), # auto-converts to python built-in float
        g=np.float16(121.0),
    )
    for serializer, deserializer in get_serializers():
        d2 = deserializer(serializer(d1))
        for k in d1:
            v1, v2 = d1[k], d2[k]
            assert type(v1) is type(v2), [type(v1), type(v2)]
            assert v1.dtype == v2.dtype
            assert np.array_equal(v1, v2)

        for special_number in [np.nan, np.infty, -np.infty]:
            result = deserializer(serializer(special_number))
            assert type(result) is type(special_number)
            assert np.isnan(result) == np.isnan(special_number)
            assert np.isinf(result) == np.isinf(special_number)


def test_pandas():
    df1 = pd.DataFrame(dict(a=[1, 2, 3], b=[True, False, False], c=["one", "two", "three"], d=[1.0, 2.0, 3.0]))
    df1["arrayed"] = list(np.arange(3 * 4).reshape([3, 4]))

    # three levels of columns
    df2 = df1.copy()
    df2.columns = pd.MultiIndex.from_tuples([(x, x, x) for x in df1.columns])

    d = dict(
        a=df1,
        b=df1.set_index(["a", "b"]),
        c=df2,
    )
    for serializer, deserializer in get_serializers():
        d2 = deserializer(serializer(d))
        for k in d:
            v1, v2 = d[k], d2[k]
            assert type(v1) is type(v2), [type(v1), type(v2)]
            assert (v1.dtypes == v2.dtypes).all()
            assert pd.DataFrame.equals(v1, v2)

        cols = [df1[c] for c in df1.columns]
        for v1, v2 in zip(
            cols,
            deserializer(serializer(cols)),
        ):
            assert type(v1) is type(v2)
            assert v1.name == v2.name


def test_polars():
    import polars as pl

    df1 = pl.DataFrame(
        dict(
            a=[1, 2, 3],
            b=[True, False, False],
            c=["one", "two", "three"],
            d=[1.0, 2.0, 3.0],
            arrayed=[[1, 2], [3, 4], [5, 6]],
        )
    )

    for serializer, deserializer in get_serializers():
        df2 = deserializer(serializer(df1))

        assert type(df1) is type(df2), [type(df1), type(df2)]
        assert df1.frame_equal(df2)

        cols = [df1.get_column(c) for c in df1.columns]
        for v1, v2 in zip(
            cols,
            deserializer(serializer(cols)),
        ):
            assert type(v1) is type(v2)
            assert v1.name == v2.name


def test_dataclasses():
    from dataclasses import dataclass

    @dataclass
    class Point:
        x: int
        y: float

    @dataclass
    class Point3d(Point):
        z: str
        w: Optional[np.ndarray] = None

    @dataclass
    class Polygon:
        points_2d: List[Point]
        point_3d: Point3d

    from antipickle.adapters import DataclassAdapter
    from antipickle import dumps, loads

    adapters = [
        DataclassAdapter(
            dict(
                point=Point,
                point_3d=Point3d,
                poly=Polygon,
            )
        )
    ]

    poly1 = Polygon(
        points_2d=[Point(1, 2.0), Point(3, 4.0)],
        point_3d=Point3d(3, 4.0, "5", w=np.zeros(1)),
    )

    packed = dumps(poly1, adapters=adapters)
    poly2 = loads(packed, adapters=adapters)
    assert poly1 == poly2


def test_pydantic():
    from pydantic import BaseModel

    class Point(BaseModel):
        x: int
        y: float

    class Point3d(Point):
        z: str
        w: Tuple[str, str] = None

    class Polygon(BaseModel):
        points_2d: List[Point]
        point_3d: Point3d

    from antipickle.adapters import PydanticAdapter
    from antipickle import dumps, loads

    adapters = [
        PydanticAdapter(
            dict(
                point=Point,
                point_3d=Point3d,
                poly=Polygon,
            )
        )
    ]

    poly1 = Polygon(
        points_2d=[Point(x=1, y=2.0), Point(x=3, y=4.0)],
        point_3d=Point3d(x=3, y=4.0, z="5", w=("a", "bc")),
    )

    packed = dumps(poly1, adapters=adapters)
    poly2 = loads(packed, adapters=adapters)
    assert poly1 == poly2


if __name__ == "__main__":
    test_pydantic()
    test_dataclasses()
    test_simple_types()
    test_numpy()
    test_pandas()
