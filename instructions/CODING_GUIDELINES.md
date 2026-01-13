# Coding Guidelines

Guidelines for code quality, testing patterns, and lint compliance.

## Python Imports

### Always at Top Level

All imports must be at the top of the file, not inside functions or methods.

```python
# GOOD - imports at top
from mymodule import MyClass
from datetime import datetime

def my_function():
    result = MyClass().do_thing()
    return result

# BAD - imports inside functions
def my_function():
    from mymodule import MyClass  # PLC0415 violation!
    result = MyClass().do_thing()
    return result
```

### Why Not Inside Functions?

The "test isolation via local imports" pattern is a misconception:

1. **Python caches modules in `sys.modules`** - re-importing returns the same reference
2. **No isolation benefit** - the module is loaded once at first import
3. **Performance overhead** - adds unnecessary import lookup each call
4. **Lint violation** - triggers PLC0415 error

For actual test isolation, use:
- Proper fixtures with setup/teardown
- Mock objects and patches
- Fresh object instances per test

## Unused Variables

### Use Underscore Prefix

When unpacking values you don't need, prefix with `_`:

```python
# GOOD - clearly indicates unused
entities, _mentions = tracker.track_mentions(doc, raw_entities)
assert len(entities) == 3

# BAD - triggers RUF059 warning
entities, mentions = tracker.track_mentions(doc, raw_entities)
# mentions never used!
```

### Loop Variables

Same rule for loop control variables:

```python
# GOOD - underscore for unused variable
for _offset, chunk_text in chunks:
    reconstructed += chunk_text

# BAD - triggers B007 warning
for offset, chunk_text in chunks:
    reconstructed += chunk_text
    # offset never used!
```

## Test File Organization

### No Decorative Section Headers

Avoid section headers that look like commented code:

```python
# BAD - triggers ERA001 (looks like commented code)
# -----------------------------------------------------------------------------
# Tests: analyze_book()
# -----------------------------------------------------------------------------

class TestAnalyzeBook:
    ...

# GOOD - use class docstrings instead
class TestAnalyzeBook:
    """Tests for analyze_book() method."""
    ...
```

The class docstring provides the same organizational benefit without triggering lint errors.

## Warning Suppression

### Use Proper Filters

When legitimate warnings need suppression, use `warnings.filterwarnings()`:

```python
import warnings
from bs4 import XMLParsedAsHTMLWarning

# Suppress at module level with clear comment explaining why
# EPUB content is XHTML but we use lxml's HTML parser for leniency
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
```

### Place After Imports

Warning filters must come after the import that defines the warning class:

```python
# GOOD - filter after imports
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# BAD - filter before import (E402 violation)
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

from bs4 import XMLParsedAsHTMLWarning  # E402: module level import not at top
```

## Lint Rules Reference

| Rule | Issue | Fix |
|------|-------|-----|
| PLC0415 | Import inside function | Move to top of file |
| ERA001 | Commented-out code | Remove or reformat |
| RUF059 | Unused unpacked variable | Prefix with `_` |
| B007 | Unused loop variable | Prefix with `_` |
| E402 | Import not at top | Move imports to top |
