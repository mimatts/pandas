# Report for assignment 4 Group 28

## Project

**Name**: Pandas

**URL**: https://github.com/pandas-dev/pandas

**Summary**

**pandas** is a Python package that provides fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive. It aims to be the fundamental high-level building block for
doing practical, **real world** data analysis in Python. Additionally, it has
the broader goal of becoming **the most powerful and flexible open source data
analysis / manipulation tool available in any language**. It is already well on
its way towards this goal.

## Onboarding experience

1. Did you choose a new project or continue on the previous one? 

    We chose a new project, *pandas* instead of our old project *TheAlgorithms/Python*.

2. If you changed the project, how did your experience differ from before?

    Our project for assignment 3 was a collection of algorithms, so it did not require any setup. In difference to pandas, which require many dependencies and a special developing setup. Furthermore, the pandas project is much more complex and difficult to understand, while the algorithms project was very straightforward.

## Effort spent

An overview of how much time each group member spent on different activities:

| **Activity** | **Jennifer Larsson** | **Michaela Mattsson** | **Maegan Peralta** | **Karlis Kristofers Velins** |
| ------------ | ------------ | ------------ | ---------- | ---------- |
| **Plenary discussions/meetings** | 4h | | | 3h |
| **Discussions within parts of the group** | 2h | | | 3h | 
| **Reading documentation** | 2h | | | 3h |
| **Configuration and setup** | 2h | | | 3h | 
| **Analyzing code/output** | 6h | | | 5h |
| **Writing documentation** | 2h | | | 1h |
| **Writing code** | 2h | | | 3h |
| **Running code** | - | | | - |

## Overview of issue(s) and work done.

1. **Enhancement issue**

    **Title**: Default negative location in pandas insert

    **URL**: https://github.com/pandas-dev/pandas/issues/49496

    **Summary**

    Previously, specifying the index for a new column was mandatory when inserting data. In order to improve the functionality, an enhancement was made to modify the insertion process. This enhancement enables the insertion of arguments without the need for a specified index and by default, the data set will be added at the end.

    **Scope** 

    insert is used in the class Dataframe, which is a very common pandas type. So the changes in this issue affects all df.insert calls.

2. **Bug issue**

    We intitially chose another issue

    **Title**: BUG: pivot_table with margins=True changes dtypes of dates

    **URL**: https://github.com/pandas-dev/pandas/issues/51581

    We managed to find a case that actually contradicted the initial issue, we made a comment on it to the author and afterwards some other people joined the discussion and ended up closing this issue since it was not a bug but rather something that would be expected to happen. It was then closed as completed! For more details please see the URL above and the comments made there.

## Requirements for the new feature or requirements affected by functionality being refactored

1. The insertion function needs to be reworked to make the parameter index optional.
2. To ensure that the added column is placed at the last index, tests should be created. 
3. Additionally, previous tests should be modified to accommodate the new parameter layout in the insertion function. 

## Code changes

### Patch

**frame.py**

```
def insert(
        self,
        column: Hashable,
        value: Scalar | AnyArrayLike,
        loc: int = -1,
        allow_duplicates: bool | lib.NoDefault = lib.no_default,
    ) -> None:

    ...

    if allow_duplicates is lib.no_default:
            allow_duplicates = False
        if allow_duplicates and not self.flags.allows_duplicate_labels:
            raise ValueError(
                "Cannot specify 'allow_duplicates=True' when "
                "'self.flags.allows_duplicate_labels' is False."
            )
        if not allow_duplicates and column in self.columns:
            # Should this be a different kind of error??
            raise ValueError(f"cannot insert {column}, already exists")
        if not isinstance(loc, int):
            raise TypeError("loc must be int")
        if loc < 0:
            loc = len(self.columns)

        value = self._sanitize_column(value)
        self._mgr.insert(loc, column, value)
```

**test_insert.py**

```
    ...

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
```

## Test results

1. The before test logs can be found [here](https://github.com/mimatts/pandas/blob/main/pandas/tests/frame/indexing/test-log-before.xml).

    **Summary**:
    * 6 passed
    * 0 failed
    * 0 skipped

2. The after test logs can be found [here](https://github.com/mimatts/pandas/blob/main/pandas/tests/frame/indexing/test-data-after.xml).

    **Summary**:
    * 8 passed
    * 0 failed
    * 0 skipped

## UML class diagram and its description

The class we were working on is part of one of the main pandas classes located under pandas/core/frame.py which creates the main structure everyone who uses this library uses for creating their data structures. The diagram was created using the Diagrams.net extension in PyCharm 

This function, which we worked on, is located in frame.py and is one of many DataFrame class'es frame.py functions. As we can see the DataFrame class is a more specific class which inherits from other base super classes. So our insert method doesn't impact the superclasses but just the actual DataFrame class which is one of the most important classes and the most used classes in the pandas library

EDIT: added more detailed description of UML diagram. For each of the classes in the diagram:

The DataFrame class is a 2-dimensional size-mutable tabular data structure with rows and columns. It is one of the most commonly used data structures in pandas and is used for data cleaning, manipulation, and analysis.

The NDFrame class and NDFrame structure stands for N-dimensional Frame, which means it is designed to work with data that has more than one dimension. It is a flexible and efficient container for storing and manipulating large and complex datasets.

The OpsMixin class provides a set of common arithmetic and comparison methods for pandas objects, such as Series and DataFrame. The purpose of the OpsMixin class is to provide a consistent and efficient way to perform arithmetic and comparison operations across different pandas objects. Some of the methods provided by the OpsMixin class include:

The PandasObject class in the pandas Python library is an abstract base class that serves as the base class for many of the core data structures in pandas, such as Series, DataFrame, and Index.

The IndexingMixin class is used to provide a consistent and efficient way to perform indexing and selection operations across different pandas objects

The  DirNamesMixin class is to provide a consistent and efficient way to access the names of columns or indexes across different pandas objects.

def insert(
        self,
        column: Hashable,
        value: Scalar | AnyArrayLike,
        loc: int = -1,
        allow_duplicates: bool | lib.NoDefault = lib.no_default,
    ) -> None:
    


![image](https://user-images.githubusercontent.com/59483828/222268436-6873393d-1059-4084-a223-1a547578164b.png)

## Overall experience

What are your main take-aways from this project? What did you learn?

Our main take-aways from this project are:
1. It can be difficult to navigate and understand a complex existing project. It took us a lot of time to understand the functionalities of different functions/classes/files.
2. It was difficult to find an issue with an appropriate scope for this assignment. 
3. All the issues in the issue tracker do not describe an actual issue with the code. Some issues in the issue tracker report expected behaviour as bugs. We had this problem with the first issue that we picked.

How did you grow as a team, using the Essence standard to evaluate yourself?

The Essence checklist can be found [here](https://docs.google.com/document/d/1cplATiqxmItaO3Zb8u7uR8hS3H0rga7LcexPhgCMHXA/edit?usp=sharing).

We are currently in the state *in place* according to the Essence standard. Since the last assignment, we have had a chance to work more as a team instead. There has been many small decisions to make, which has made us have more meetings with shorter notice, and in general be more agile. There is still room for improvement, but the team work has definately improved since the last assignment.

