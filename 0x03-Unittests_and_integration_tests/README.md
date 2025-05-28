# GitHub Org Utils – Python Unit Testing

This project is a Python utility module that provides helper functions for working with nested dictionaries, fetching JSON data from URLs, and memoizing method results. The codebase is structured with a strong emphasis on unit testing.

---

## Features

- `access_nested_map`: Access values in nested dictionaries using a list or tuple of keys.
- `get_json`: Retrieve and parse JSON content from a given HTTP URL.
- `memoize`: Decorator that caches method results to optimize repeated calls.

---

## Testing

Unit tests are written using Python’s built-in `unittest` framework and enhanced with `parameterized` to cover multiple input scenarios efficiently.

### Tests for `access_nested_map`

Two categories of tests are implemented:

1. **Valid access tests**: 
   These tests confirm that `access_nested_map` returns the correct value for given nested dictionary paths.

   Example scenarios:
   - `{"a": 1}, path=("a",)` → returns `1`
   - `{"a": {"b": 2}}, path=("a",)` → returns `{"b": 2}`
   - `{"a": {"b": 2}}, path=("a", "b")` → returns `2`

2. **Exception tests**:
   These tests verify that the function raises a `KeyError` when the key path is invalid or missing in the dictionary.

   Example scenarios:
   - `{}`, path `("a",)`
   - `{"a": 1}`, path `("a", "b")`

Each test case is parameterized to keep the test logic concise and readable.

To run the tests:
```bash
python test_utils.py
```
