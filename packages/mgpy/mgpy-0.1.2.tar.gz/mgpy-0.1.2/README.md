# `mgpy` ("Magpie")
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Tests](https://github.com/phistoh/mgpy/raw/main/docs/badges/tests.svg)](https://docs.pytest.org/en/8.2.x/) [![Coverage](https://github.com/phistoh/mgpy/raw/main/docs/badges/coverage.svg)](https://github.com/pytest-dev/pytest-cov)


A small package containing simple, useful methods I regularly use and don't want to manually copy into several projects.

Contains the following modules:

## `mgstr` ("Magister")
<details>
<summary>Contains methods relating to strings.</summary>

### *function* `log_print`

```python
log_print(s: str, level: Loglevel = Loglevel.INFO, time_format: str = "%Y-%m-%d %H:%M:%S")
```

Takes a string and outputs it with an additional prefix indicating importance.

**Args:**

 - **`s`** (`str`):  The string which will be output
 - **`level`** (`Loglevel`, optional):  The prefix indicating importance. Defaults to `Loglevel.INFO`.
 - **`time_format`** (`str`, optional): A (C-time adherent) string to format the time. Defaults to `%Y-%m-%d %H:%M:%S`

### *function* `truncate_string`

```python
truncate_string(s: str, length: int, ellipsis: str = '...') → str
```

Takes a string, truncates it to the given length, adding a given ellipsis.

**Args:**

 - **`s`** (`str`):  The string which will be shortened.
 - **`length`** (`int`):  The length of the shortened string including the length of the ellipsis.
 - **`ellipsis`** (`str`, optional):  An optional ellipsis which will be appended. Defaults to `"..."`.

**Returns:**

 - **`str`**:  A truncated version of the string with given length (and ellipsis)

### *function* `insert_line_into_string`

```python
insert_line_into_string(line: str, s: str, pos: int) → str
```

Takes two strings and inserts the first one into the second one as a new line at the given position.

**Args:**

 - **`line`** (`str`):  The line to insert.
 - **`s`** (`str`):  The (potential multi-line) string in which to insert `line`.
 - **`pos`** (`int`):  The line number of the newly inserted line. Uses Python's `List.insert()` position syntax—negative indices, e.g. `-1`, inserts `line` *before* the last element.

**Returns:**

 - **`str`**:  A new string containing line at the given line number.

### *class* `Loglevel`
A string enum defining importance levels for usage in the 'log_print' method

**Members:**
- `INFO = "Information"`: Used to indicate an informational output.
- `WARNING = "Warning"`: Used to indicate a warning.
- `ERROR = "ERROR"`: Used to indicate an error.
</details>

## `mgcl` ("Magical")
<details>
<summary>Contains methods to work with colors and convert between different representations.</summary>

*tbd.*
</details>

## `mgnet` ("Magnet")
<details>
<summary>Contains network related methods.</summary>

*tbd.*
</details>

## `mgnum` ("Magnum")
<details>
<summary>Contains methods relating to numbers and their representation.</summary>

### *function* `generate_human_readable_number`

```python
generate_human_readable_number(
    number: int,
    suffixes: list[str] = None,
    decimal_separator: str = '.'
) → str
```

Takes a number and returns a 'human readable' string. E.g., `1500000` → `1.5M`

**Args:**

 - **`number`** (`int`):  The number to represent.
 - **`suffixes`** (`list[str]`, optional):  A list of ascendingly sorted suffixes for each order of magnitude. Defaults to `["k", "M", "G", "T"]`.
 - **`decimal_separator`** (`str`, optional):  The decimal separator. Defaults to `"."`.

**Returns:**

 - **`str`**:  The human readable string.
</details>

## `mgte` ("Mogote")
<details>
<summary>Contains methods to work with time and date.</summary>

*tbd.*
</details>

## `mgmin` ("Megumin")
<details>
<summary>Contains methods which don't fall into the other categories.</summary>

*tbd.*
</details>

---

*Module descriptions were automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs).*
