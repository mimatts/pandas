"""
test_insert is specifically for the DataFrame.insert method; not to be
confused with tests with "insert" in their names that are really testing
__setitem__.
"""
import numpy as np
import pytest

from pandas.errors import PerformanceWarning

from pandas import (
    DataFrame,
    Index,
)
import pandas._testing as tm


class TestDataFrameInsert:
    def test_insert(self):
        df = DataFrame(
            np.random.randn(5, 3), index=np.arange(5), columns=["c", "b", "a"]
        )

        df.insert("foo", df["a"], 0)
        tm.assert_index_equal(df.columns, Index(["foo", "c", "b", "a"]))
        tm.assert_series_equal(df["a"], df["foo"], check_names=False)

        df.insert("bar", df["c"], 2)
        tm.assert_index_equal(df.columns, Index(["foo", "c", "bar", "b", "a"]))
        tm.assert_almost_equal(df["c"], df["bar"], check_names=False)

        with pytest.raises(ValueError, match="already exists"):
            df.insert("a", df["b"], 1)

        msg = "cannot insert c, already exists"
        with pytest.raises(ValueError, match=msg):
            df.insert("c", df["b"], 1)

        df.columns.name = "some_name"
        # preserve columns name field
        df.insert("baz", df["c"], 0)
        assert df.columns.name == "some_name"

    def test_insert_column_bug_4032(self):
        # GH#4032, inserting a column and renaming causing errors
        df = DataFrame({"b": [1.1, 2.2]})

        df = df.rename(columns={})
        df.insert("a", [1, 2], 0)
        result = df.rename(columns={})

        str(result)
        expected = DataFrame([[1, 1.1], [2, 2.2]], columns=["a", "b"])
        tm.assert_frame_equal(result, expected)

        df.insert("c", [1.3, 2.3], 0)
        result = df.rename(columns={})

        str(result)
        expected = DataFrame([[1.3, 1, 1.1], [2.3, 2, 2.2]], columns=["c", "a", "b"])
        tm.assert_frame_equal(result, expected)

    def test_insert_with_columns_dups(self):
        # GH#14291
        df = DataFrame()
        df.insert("A", ["g", "h", "i"], 0, allow_duplicates=True)
        df.insert("A", ["d", "e", "f"], 0, allow_duplicates=True)
        df.insert("A", ["a", "b", "c"], 0, allow_duplicates=True)
        exp = DataFrame(
            [["a", "d", "g"], ["b", "e", "h"], ["c", "f", "i"]], columns=["A", "A", "A"]
        )
        tm.assert_frame_equal(df, exp)

    def test_insert_item_cache(self, using_array_manager):
        df = DataFrame(np.random.randn(4, 3))
        ser = df[0]

        if using_array_manager:
            expected_warning = None
        else:
            # with BlockManager warn about high fragmentation of single dtype
            expected_warning = PerformanceWarning

        with tm.assert_produces_warning(expected_warning):
            for n in range(100):
                df[n + 3] = df[1] * n

        ser.values[0] = 99

        assert df.iloc[0, 0] == df[0][0]

    def test_insert_EA_no_warning(self):
        # PerformanceWarning about fragmented frame should not be raised when
        # using EAs (https://github.com/pandas-dev/pandas/issues/44098)
        df = DataFrame(np.random.randint(0, 100, size=(3, 100)), dtype="Int64")
        with tm.assert_produces_warning(None):
            df["a"] = np.array([1, 2, 3])

    def test_insert_frame(self):
        # GH#42403
        df = DataFrame({"col1": [1, 2], "col2": [3, 4]})

        msg = r"Expected a 1D array, got an array with shape \(2, 2\)"
        with pytest.raises(ValueError, match=msg):
            df.insert("newcol", df, 1)

    def test_insert_no_index(self):
        df = DataFrame()
        df.insert("A", ["g", "h", "i"], allow_duplicates=True)
        df.insert("A", ["d", "e", "f"], allow_duplicates=True)
        df.insert("A", ["a", "b", "c"], allow_duplicates=True)
        exp = DataFrame(
            [["g", "d", "a"], ["h", "e", "b"], ["i", "f", "c"]], columns=["A", "A", "A"]
        )
        tm.assert_frame_equal(df, exp)

    def test_insert_back(self):
        # test case to check that loc argument has a default value of -1
        df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        df.insert("c", [7, 8, 9])
        exp = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        tm.assert_frame_equal(df, exp)