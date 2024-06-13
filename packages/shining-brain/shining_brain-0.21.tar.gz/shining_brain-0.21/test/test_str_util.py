import pytest

from shining_brain.str_util import format_text


@pytest.mark.parametrize("text, expected", [
    ('123', '123'),
    ('123.0', '123.00'),
    ('123.456', '123.46'),
    ('Hello', 'Hello')
])
def test_format_text(text, expected):
    assert format_text(text) == expected
