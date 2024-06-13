# html-compare

Python library for comparing HTML snippets. Intentionally lacking any external dependencies. Ported from Django internal testing utilities [here](https://github.com/django/django/blob/main/django/test/html.py).


## Usage
```python

def test_html_equals():
    # Attributes should be significant, but whitepsace and quote-style should not be significant
    assert html_equal("<a data-foo='bar'>Hi\n</a>", '<a data-foo="bar"> Hi </a>')
```
