# GitHub Org Utils – Python Unit Testing

This project is a Python-based utility module that includes helper functions for working with nested dictionaries, fetching JSON from URLs, and memoizing method results. It's designed to be test-driven, with a strong focus on **unit testing using `unittest` and `parameterized`**.

---

## Features

- `access_nested_map`: Safely access values deep within nested dictionaries using a sequence of keys.
- `get_json`: Fetch and parse JSON from a remote URL.
- `memoize`: Decorator to cache method results per instance to improve performance.
- Clean and isolated unit tests for each utility function.

---

## Testing

The project includes comprehensive unit tests using the built-in `unittest` framework, enhanced by `parameterized` to run multiple input scenarios in a clean, readable way.

Each function is tested for expected behavior and edge cases (like invalid input or errors).

---

More sections coming soon...
